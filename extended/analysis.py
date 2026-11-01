"""Extended working paper replication and diagnostic extension using the archived processed data.
Run: python analysis.py. Does not download new data or overwrite the earlier repository.
"""
from pathlib import Path
import json,sys,hashlib,warnings
import numpy as np,pandas as pd,scipy,statsmodels
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import GLSAR
from statsmodels.tsa.stattools import adfuller,coint
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
HAC=dict(cov_type='HAC',cov_kwds={'maxlags':3},use_t=False)

def prep(raw,u):
 d=pd.DataFrame({v:raw[f'{v}_{u}'] for v in ['I','Y','U','FDI']})
 d['fx']=raw.fx;d['gap_pct']=raw.gap_pct
 d['dI']=d.I.diff();d['dY']=d.Y.diff();d['dFDI']=d.FDI.diff()
 d['dI_lag']=d.dI.shift();d['dY_lag']=d.dY.shift()
 lr=smf.ols('I ~ Y',d).fit();d['ECT']=lr.resid.shift()
 d['covid']=(d.index==2020).astype(int)
 return d

def row(label,m,end,u):
 names=list(m.params.index);ci=m.conf_int()
 plain=smf.ols(m.model.formula,m.model.data.frame.loc[m.model.data.row_labels]).fit() if hasattr(m.model,'formula') else None
 bg=acorr_breusch_godfrey(plain,nlags=2)[1] if plain is not None else np.nan
 return [dict(model=label,end=end,currency=u,term=v,coefficient=m.params[v],se=m.bse[v],p=m.pvalues[v],lo=ci.loc[v,0],hi=ci.loc[v,1],n=int(m.nobs),bg_p=bg) for v in names]

def main():
 raw={e:pd.read_csv(ROOT/'data'/f'fdi_data_1981_{e}.csv',index_col='year') for e in [2018,2024]}
 pd.testing.assert_frame_equal(raw[2018],raw[2024].loc[raw[2018].index],check_exact=False,rtol=1e-12)
 adf=[];eg=[];desc=[];models=[];samples={}
 for end,r in raw.items():
  assert r.notna().all().all() and r.index.is_unique
  for u in ['usd','cad']:
   d=prep(r,u);samples[end,u]=d
   for v in ['I','Y','U','FDI']:
    s=d[v];desc.append(dict(end=end,currency=u,variable=v,n=len(s),mean=s.mean(),sd=s.std(),minimum=s.min(),maximum=s.max()))
   for v in ['I','Y','U','FDI','fx']:
    for label,kwargs in [('default AIC',dict(autolag='AIC')),('max3 BIC',dict(maxlag=3,autolag='BIC'))]:
     for transform,reg in [('level','ct'),('difference','c')]:
      series=d[v] if transform=='level' else d[v].diff().dropna()
      test=adfuller(series,regression=reg,**kwargs)
      adf.append(dict(end=end,currency=u,variable=v,selection=label,transform=transform,stat=test[0],p=test[1],lags=test[2],n=test[3]))
   for label,kwargs in [('default AIC',dict(autolag='aic')),('max3 BIC',dict(maxlag=3,autolag='bic'))]:
    test=coint(d.I,d.Y,trend='c',**kwargs);eg.append(dict(end=end,currency=u,selection=label,stat=test[0],p=test[1]))
   formulas={'ECM':'dI ~ dY + U + FDI + ECT','Change level FDI':'dI ~ dY + U + FDI','Change level FDI FX':'dI ~ dY + U + FDI + fx','Change differenced FDI':'dI ~ dY + U + dFDI'}
   for label,formula in formulas.items():
    if end==2024:formula+=' + covid'
    m=smf.ols(formula,d).fit(**HAC);models+=row(label,m,end,u)
   # Common observations for comparison of lag structures, not automatic selection.
   common=d.dropna()
   for label,formula in [('Common ECM','dI ~ dY + U + FDI + ECT'),('Common ECM lag Y','dI ~ dY + dY_lag + U + FDI + ECT'),('Common ECM lag I Y','dI ~ dY + dY_lag + dI_lag + U + FDI + ECT')]:
    if end==2024:formula+=' + covid'
    models+=row(label,smf.ols(formula,common).fit(**HAC),end,u)
 d=samples[2018,'usd']
 ols=smf.ols('I ~ Y + U + FDI',d).fit()
 ar=GLSAR.from_formula('I ~ Y + U + FDI',d,rho=1).iterative_fit(maxiter=50)
 # GLSAR diagnostics are not reconstructed as plain OLS diagnostics.
 for label,m in [('OLS',ols),('AR1',ar)]:
  for term in m.params.index:
   ci=m.conf_int().loc[term]
   models.append(dict(model=label,end=2018,currency='usd',term=term,coefficient=m.params[term],se=m.bse[term],p=m.pvalues[term],lo=ci.iloc[0],hi=ci.iloc[1],n=int(m.nobs),bg_p=np.nan))
 inter=smf.ols('dI ~ dY + U + FDI + FDI:U + ECT',d).fit(**HAC)
 models+=row('Interaction',inter,2018,'usd')
 marginal=[]
 for q in [.25,.5,.75]:
  val=d.loc[inter.model.data.row_labels,'U'].quantile(q);c=np.zeros(len(inter.params));c[inter.params.index.get_loc('FDI')]=1;c[inter.params.index.get_loc('FDI:U')]=val
  tt=inter.t_test(c);ci=np.asarray(tt.conf_int()).ravel()
  marginal.append(dict(slack_quantile=q,slack=val,effect=float(np.asarray(tt.effect).ravel()[0]),se=float(np.asarray(tt.sd).ravel()[0]),p=float(tt.pvalue),lo=ci[0],hi=ci[1]))
 pd.DataFrame(marginal).to_csv(OUT/'interaction_marginal_effects.csv',index=False)
 sensitivity=[]
 for u in ['usd','cad']:
  dd=samples[2018,u]
  formula='dI ~ dY + U + FDI + ECT' if u=='usd' else 'dI ~ dY + U + FDI'
  for lag in [1,3,4]:
   m=smf.ols(formula,dd).fit(cov_type='HAC',cov_kwds={'maxlags':lag},use_t=False)
   sensitivity.append(dict(currency=u,hac_lags=lag,coefficient=m.params.FDI,se=m.bse.FDI,p=m.pvalues.FDI))
 pd.DataFrame(sensitivity).to_csv(OUT/'hac_sensitivity.csv',index=False)
 influence=[]
 for u in ['usd','cad']:
  dd=samples[2018,u];formula='dI ~ dY + U + FDI + ECT' if u=='usd' else 'dI ~ dY + U + FDI'
  dd=dd.dropna(subset=['dI','dY','U','FDI','ECT'])
  for yr in dd.index:
   m=smf.ols(formula,dd.drop(index=yr)).fit()
   # Coefficient influence only: deletion creates gaps, so do not report HAC/BG inference.
   influence.append(dict(currency=u,omitted_year=int(yr),coefficient=m.params.FDI))
 pd.DataFrame(influence).to_csv(OUT/'leave_one_out.csv',index=False)
 for name,rows in [('descriptive',desc),('adf',adf),('cointegration',eg),('model_estimates',models)]:pd.DataFrame(rows).to_csv(OUT/(name+'.csv'),index=False)
 # Figures use archived data, with no external imagery.
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
 r=raw[2018];fig,ax=plt.subplots(2,1,figsize=(7,5),sharex=True)
 ax[0].plot(r.index,r.I_usd,label='Business investment',color='#205b83');ax[0].plot(r.index,r.FDI_usd,label='FDI net inflows',color='#b96731');ax[0].set_ylabel('Current US$ billions');ax[0].legend(frameon=False)
 ax[1].bar(r.index,r.gap_pct,color='#77858a');ax[1].axhline(0,color='black',lw=.7);ax[1].set_ylabel('Output gap (%)');ax[1].set_xlabel('Year')
 fig.tight_layout();fig.savefig(FIG/'series.png',dpi=220);plt.close(fig)
 mdf=pd.DataFrame(models);sels=[('OLS','usd','FDI'),('AR1','usd','FDI'),('ECM','usd','FDI'),('Change level FDI','cad','FDI'),('Change level FDI FX','cad','FDI'),('Change differenced FDI','usd','dFDI')]
 fig,ax=plt.subplots(figsize=(7,3.7))
 for j,(model,u,term) in enumerate(sels):
  rr=mdf.query('end==2018 and model==@model and currency==@u and term==@term').iloc[0];y=len(sels)-j
  ax.errorbar(rr.coefficient,y,xerr=[[rr.coefficient-rr.lo],[rr.hi-rr.coefficient]],fmt='o',color='#205b83' if u=='usd' else '#b96731',capsize=3)
 ax.set_yticks(range(1,len(sels)+1),[f'{a} ({b.upper()}; {c})' for a,b,c in sels][::-1]);ax.axvline(0,color='gray',lw=.8);ax.set_xlabel('Coefficient and 95% confidence interval');fig.tight_layout();fig.savefig(FIG/'coefficients.png',dpi=220);plt.close(fig)
 fig,axes=plt.subplots(1,2,figsize=(7,2.8))
 for ax,u in zip(axes,['usd','cad']):
  dd=samples[2018,u];formula='dI ~ dY + U + FDI + ECT' if u=='usd' else 'dI ~ dY + U + FDI'
  m=smf.ols(formula,dd).fit();plot_acf(m.resid,lags=6,ax=ax,title=u.upper()+' residual ACF',zero=False)
 fig.tight_layout();fig.savefig(FIG/'residual_acf.png',dpi=220);plt.close(fig)
 versions={'python':sys.version.split()[0],'numpy':np.__version__,'pandas':pd.__version__,'statsmodels':statsmodels.__version__,'scipy':scipy.__version__}
 versions['data_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data').glob('*.csv')}
 (OUT/'environment.json').write_text(json.dumps(versions,indent=2))
 print('COINTEGRATION');print(pd.DataFrame(eg).to_string(index=False))
 print('MAIN TERMS');print(mdf.query('end==2018 and term in ["FDI","ECT","dFDI"] and not model.str.startswith("Common")')[['model','currency','term','coefficient','p','n','bg_p']].to_string(index=False))
 print('ADF SENSITIVITY');print(pd.DataFrame(adf).query('end==2018 and transform=="level"')[['currency','variable','selection','p','lags']].to_string(index=False))
 print('LOO');print(pd.DataFrame(influence).groupby('currency').coefficient.agg(['min','max']).to_string())
if __name__=='__main__':
 with warnings.catch_warnings():
  warnings.filterwarnings('ignore',category=FutureWarning)
  main()

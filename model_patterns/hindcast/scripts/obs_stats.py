import numpy as np, pandas as pd, os
from scipy import stats
H=os.path.join(os.path.dirname(__file__),".."); D=os.path.join(H,"data")
obs=pd.read_csv(os.path.join(D,"obs_ca_winter_precip_enso.csv"))
rows=[]
for (s,reg),g in obs.groupby(["season","region"]):
    for idx in ["ONI_NDJ","RONI_NDJ"]:
        for p0,p1 in [(1950,2025),(1982,2025)]:
            h=g[(g.decyear>=p0)&(g.decyear<=p1)].dropna(subset=[idx])
            x=h[idx].values
            lr=stats.linregress(x,h.pct_normal_9120); lz=stats.linregress(x,h.z_9120)
            rs=stats.spearmanr(x,h.pct_normal_9120)[0]
            # nonlinearity: quadratic term, and slope over El Nino years only
            X=np.c_[np.ones_like(x),x,x**2]; b,res,_,_=np.linalg.lstsq(X,h.pct_normal_9120.values,rcond=None)
            e=h[h[idx]>=0.5]; le=stats.linregress(e[idx],e.pct_normal_9120)
            rows.append(dict(season=s,region=reg,index=idx,period=f"{p0}-{p1}",n=len(h),slope_pct_per_C=lr.slope,slope_se=lr.stderr,
              r=lr.rvalue,p=lr.pvalue,spearman=rs,slope_z_per_C=lz.slope,quad_coef=b[2],
              slope_ElNino_only=le.slope,slope_ElNino_only_se=le.stderr,n_ElNino=len(e)))
st=pd.DataFrame(rows); st.to_csv(os.path.join(D,"obs_regression_stats.csv"),index=False,float_format="%.3f")
pd.set_option("display.width",250)
print(st[st.region!="SoCal_d67"].round(2).to_string(index=False))
print("\nSoCal div6+7 sensitivity:"); print(st[st.region=="SoCal_d67"].round(2).to_string(index=False))
# strong-event tables
for idx in ["ONI_NDJ","RONI_NDJ"]:
    w=obs[(obs[idx]>=1.5)&(obs.region!="SoCal_d67")].pivot_table(index=["winter","ONI_NDJ","RONI_NDJ"],columns=["region","season"],values="pct_normal_9120")
    print(f"\nEvents with {idx}>=1.5 (% of 1991-2020 normal):"); print(w.round(0).to_string())
    print("composite mean:",w.mean().round(0).to_dict()); print("composite median:",w.median().round(0).to_dict())
    print("fraction >100%:",(w>100).mean().round(2).to_dict())
    w.round(1).to_csv(os.path.join(D,f"obs_strong_events_{idx.split('_')[0]}_ge1.5.csv"))
# residuals of strongest events from linear fit (1950-2025, ONI)
print("\nResiduals from linear fit (pp of normal), 1950-2025:")
for idx in ["ONI_NDJ","RONI_NDJ"]:
  for (s,reg),g in obs[obs.region!="SoCal_d67"].groupby(["season","region"]):
    g=g.dropna(subset=[idx]); lr=stats.linregress(g[idx],g.pct_normal_9120)
    g=g.assign(pred=lr.intercept+lr.slope*g[idx]); g["resid"]=g.pct_normal_9120-g.pred
    sel=g[g.decyear.isin([1957,1965,1972,1982,1987,1991,1997,2009,2015,2023])]
    print(idx,s,reg," ".join(f"{int(r.decyear)}:{r.pct_normal_9120:.0f}(pred {r.pred:.0f})" for r in sel.itertuples()))
# rank of 2015-16 in record
for s in ["DJF","JFM"]:
    g=obs[(obs.region=="SoCal_d6")&(obs.season==s)]
    print(s,"SoCal 2015-16 % normal",round(g[g.decyear==2015].pct_normal_9120.iloc[0]),"rank (wettest=1) of",len(g),int((g.pct_normal_9120>g[g.decyear==2015].pct_normal_9120.iloc[0]).sum()+1))
# ---- nonlinearity & outlier diagnostics (1950-2025)
print("\nQuadratic-term t-stat, residual SD, 2015 residual z, tercile stats:")
diag=[]
for idx in ["ONI_NDJ","RONI_NDJ"]:
  for (s,reg),g in obs[obs.region!="SoCal_d67"].groupby(["season","region"]):
    g=g.dropna(subset=[idx]); x=g[idx].values; y=g.pct_normal_9120.values
    X=np.c_[np.ones_like(x),x,x**2]; b=np.linalg.lstsq(X,y,rcond=None)[0]; res=y-X@b
    s2=res@res/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    lr=stats.linregress(x,y); r1=y-(lr.intercept+lr.slope*x); sdr=r1.std(ddof=2)
    r15=r1[g.decyear.values==2015][0]
    # terciles from 1991-2020 winters (Dec-year labels 1990-2019)
    ref=g[(g.decyear>=1990)&(g.decyear<=2019)].pct_normal_9120; t1,t2=np.percentile(ref,[100/3,200/3])
    st_=g[g[idx]>=1.5].pct_normal_9120
    d=dict(index=idx,season=s,region=reg,quad_t=b[2]/se[2],resid_sd=sdr,resid2015=r15,resid2015_z=r15/sdr,
           n_strong=len(st_),n_upper_tercile=int((st_>t2).sum()),n_lower_tercile=int((st_<t1).sum()),n_above_normal=int((st_>100).sum()),
           all_yrs_frac_above_normal=(y>100).mean())
    diag.append(d)
dg=pd.DataFrame(diag); print(dg.round(2).to_string(index=False)); dg.to_csv(os.path.join(D,"obs_nonlinearity_diagnostics.csv"),index=False,float_format="%.3f")

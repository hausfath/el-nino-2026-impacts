import numpy as np, pandas as pd, os, sys
from scipy import stats
H=os.path.join(os.path.dirname(__file__),".."); D=os.path.join(H,"data")
SUF=sys.argv[1] if len(sys.argv)>1 else ""
ACTIVE=["CanSIPS-IC4","NCEP-CFSv2","NASA-GEOSS2S","COLA-RSMAS-CCSM4","COLA-RSMAS-CESM1","GFDL-SPEAR"]
R=pd.read_csv(os.path.join(D,f"nmme_regression_vs_obs{SUF}.csv"))
out=[]
print("Slope ratio model/obs (same years, ONI) and model slopes (pp of normal per degC):")
for (reg,sn),g in R[R.region.isin(["SoCal_d6","NorCal_d2"])].groupby(["region","season"]):
    for lab,h in [("all",g),("active",g[g.model.isin(ACTIVE)])]:
        d=dict(region=reg,season=sn,set=lab,n_models=len(h),ratio_median=h.ratio_vs_obs_sameyrs.median(),ratio_min=h.ratio_vs_obs_sameyrs.min(),ratio_max=h.ratio_vs_obs_sameyrs.max(),
               ratio1950_median=h.ratio_vs_obs_1950_2025.median(),model_slope_median=h.model_slope_pct_per_C.median(),model_slope_min=h.model_slope_pct_per_C.min(),model_slope_max=h.model_slope_pct_per_C.max(),
               n_ratio_gt1=int((h.ratio_vs_obs_sameyrs>1).sum()),skill_median=h.precip_skill_r.median())
        out.append(d)
S=pd.DataFrame(out); print(S.round(2).to_string(index=False)); S.to_csv(os.path.join(D,f"summary_slope_ratios{SUF}.csv"),index=False,float_format="%.3f")
# obs slope uncertainty -> ratio uncertainty
ost=pd.read_csv(os.path.join(D,"obs_regression_stats.csv"))
print("\nObs slope 95% CI (ONI, 1950-2025):")
for r in ost[(ost["index"]=="ONI_NDJ")&(ost.period=="1950-2025")&(ost.region!="SoCal_d67")].itertuples():
    print(f"  {r.region} {r.season}: {r.slope_pct_per_C:.1f} [{r.slope_pct_per_C-1.99*r.slope_se:.1f}, {r.slope_pct_per_C+1.99*r.slope_se:.1f}] pp/degC")
# member-level: probability of dry outcome in strong model El Ninos
P=pd.read_csv(os.path.join(D,f"nmme_sepinit_regional_series{SUF}.csv"))
Mm=pd.read_csv(os.path.join(D,f"nmme_member_pct_normal{SUF}.csv"))
n34=P[["model","year","nino34_NDJ_model"]].drop_duplicates()
Mm=Mm.merge(n34,on=["model","year"])
print("\nMember-level outcomes in hindcast years with model ens-mean NDJ Nino3.4 >= 2.0 degC (1982-2025, excl. 2026):")
rows=[]
for (reg,sn),g in Mm[(Mm.nino34_NDJ_model>=2.0)&(Mm.year<=2025)].groupby(["region","season"]):
    per=g.groupby("model").apply(lambda h: pd.Series(dict(n=len(h),yrs=h.year.nunique(),below100=(h.pct_normal<100).mean(),below70=(h.pct_normal<70).mean(),median=h.pct_normal.median())),include_groups=False)
    rows.append(dict(region=reg,season=sn,n_members=len(g),models=g.model.nunique(),frac_below_normal_pooled=(g.pct_normal<100).mean(),frac_below70_pooled=(g.pct_normal<70).mean(),
                     frac_below_normal_model_median=per.below100.median(),median_pct=g.pct_normal.median()))
    print(reg,sn); print(per.round(2).to_string())
MR=pd.DataFrame(rows); print(MR.round(2).to_string(index=False)); MR.to_csv(os.path.join(D,f"summary_member_strong_events{SUF}.csv"),index=False,float_format="%.3f")
obs=pd.read_csv(os.path.join(D,"obs_ca_winter_precip_enso.csv"))
for thr in [1.5,2.0]:
    o=obs[(obs.ONI_NDJ>=thr)&obs.region.isin(["SoCal_d6","NorCal_d2"])]
    print(f"Observed ONI>={thr}: frac below normal:",o.groupby(["region","season"]).pct_normal_9120.apply(lambda x: f"{(x<100).sum()}/{len(x)}").to_dict(), " below 70%:",o.groupby(["region","season"]).pct_normal_9120.apply(lambda x: f"{(x<70).sum()}/{len(x)}").to_dict())
# climatological base rate of <70% and <100% in models (all years) vs obs
print("\nBase rates, all years 1982-2025: model members <100%:",Mm[Mm.year<=2025].groupby(["region","season"]).pct_normal.apply(lambda x:(x<100).mean()).round(2).to_dict())
print("obs <100% 1982-2025:",obs[(obs.decyear>=1982)&obs.region.isin(["SoCal_d6","NorCal_d2"])].groupby(["region","season"]).pct_normal_9120.apply(lambda x:(x<100).mean()).round(2).to_dict())
# 2015 & 1997 hit/miss
E=P[P.year.isin([1982,1997,2015,2023])&P.region.isin(["SoCal_d6","NorCal_d2"])]
print("\nHit/miss (ens-mean >100% = wet call):")
for (y,reg,sn),g in E.groupby(["year","region","season"]):
    ob=g.obs_pct_normal.iloc[0]
    print(f"  {y}-{str(y+1)[2:]} {reg} {sn}: obs {ob:.0f}% | models wet call {int((g.pct_normal>100).sum())}/{len(g)}, model range {g.pct_normal.min():.0f}-{g.pct_normal.max():.0f}%, median {g.pct_normal.median():.0f}%")
# 2026
F=P[(P.year==2026)&P.region.isin(["SoCal_d6","NorCal_d2"])]
print("\n2026 Sep-init:")
print(F[["model","region","season","nino34_NDJ_model","pct_normal","frac_members_above_normal","n_mem"]].round(2).to_string(index=False))
print(F.groupby(["region","season"]).pct_normal.agg(["mean","median","min","max","count"]).round(0).to_string())
print("model NDJ Nino3.4 2026 (own 1991-2020 clim):",F.drop_duplicates("model").set_index("model").nino34_NDJ_model.round(2).to_dict())
# linear extrapolation of observed fit
print("\nObserved linear fit (ONI, 1950-2025) evaluated at x (pure extrapolation beyond max obs ONI NDJ %.2f):"%obs.ONI_NDJ.max())
for reg in ["SoCal_d6","NorCal_d2"]:
    for sn in ["DJF","JFM"]:
        o=obs[(obs.region==reg)&(obs.season==sn)].dropna(subset=["ONI_NDJ"]); lr=stats.linregress(o.ONI_NDJ,o.pct_normal_9120)
        print(f"  {reg} {sn}: " + ", ".join(f"x={x}: {lr.intercept+lr.slope*x:.0f}%" for x in [2.5,3.3,3.9]))

"""NMME Sep-init regional precip & Nino3.4: anomalies, regressions vs obs, event table, 2026 forecasts."""
import numpy as np, pandas as pd, xarray as xr, os, glob, sys
SPLIT = "--split" in sys.argv   # sensitivity: separate 1982-1998 / 1999-2020 climatologies for CFSR-initialised models
SPLIT_MODELS={"NCEP-CFSv2","COLA-RSMAS-CCSM4","COLA-RSMAS-CESM1"}
SUF = "_splitclim" if SPLIT else ""
from scipy import stats
H=os.path.join(os.path.dirname(__file__),".."); D=os.path.join(H,"data"); RAW=os.path.join(D,"nmme_raw")
W=pd.read_csv(os.path.join(D,"model_region_weights.csv"))
REG=["SoCal_d6","NorCal_d2","SoCal_box","NorCal_box"]
SEAS={"DJF":[3.5,4.5,5.5],"JFM":[4.5,5.5,6.5]}   # S=Sep: L=0.5 Sep ... 3.5 Dec, 4.5 Jan, 5.5 Feb, 6.5 Mar
NDJ=[2.5,3.5,4.5]
MODELS=sorted({os.path.basename(f).split("_")[0] for f in glob.glob(os.path.join(RAW,"*_prec.nc"))})
def wavg(da,reg):
    w=W.set_index(["Y","X"])[reg].to_xarray().fillna(0)
    w=w.sel(Y=da.Y,X=da.X)
    return (da*w).sum(["X","Y"],skipna=False)/w.sum()   # skipna=False: all-NaN (absent) members stay NaN, not 0
recs=[]      # per model/year/member-agnostic ens-mean records
memrecs=[]
for m in MODELS:
    for fp in sorted(glob.glob(os.path.join(RAW,f"{m}_*_prec.nc"))):
        stream=os.path.basename(fp).split("_")[1]
        fs=fp.replace("_prec.nc","_nino34.nc")
        p=xr.open_dataarray(fp,decode_times=False)
        yrs=np.round(1960+(p.S.values-8)/12).astype(int)
        n34=None
        if os.path.exists(fs):
            s=xr.open_dataarray(fs,decode_times=False)
            sy=np.round(1960+(s.S.values-8)/12).astype(int)
            n34=s.sel(L=NDJ,method="nearest").mean("L")   # (S,M)
            n34=pd.DataFrame(n34.values.T if n34.dims[0]=="M" else n34.values,index=sy)
        for reg in REG:
            r=wavg(p,reg)
            for sn,Ls in SEAS.items():
                x=r.sel(L=Ls,method="nearest").mean("L")
                x=x.transpose("S","M").values
                for i,y in enumerate(yrs):
                    for j in range(x.shape[1]):
                        if np.isfinite(x[i,j]): memrecs.append(dict(model=m,stream=stream,year=y,member=j,region=reg,season=sn,prec=x[i,j]))
        if n34 is not None:
            for y in n34.index:
                for j,v in enumerate(n34.loc[y].values):
                    if np.isfinite(v): memrecs.append(dict(model=m,stream=stream,year=y,member=j,region="nino34",season="NDJ",prec=v))
M=pd.DataFrame(memrecs)
# if a year appears in both streams keep hindcast
M=M.sort_values("stream",ascending=False)  # HINDCAST before FORECAST
dup=M.groupby(["model","year"]).stream.transform(lambda s: s.iloc[0])
M=M[M.stream==dup]
out=[]; clim_info={}; CL={}
for (m,reg,sn),g in M.groupby(["model","region","season"]):
    em=g.groupby("year").prec.mean(); yrs=em.index
    cy=[y for y in yrs if 1990<=y<=2019]
    if len(cy)>=20: cp=f"1991-2020 target (Sep-init years {min(cy)}-{max(cy)}, n={len(cy)})"
    else: cy=[y for y in yrs if y<=2025]; cp=f"{min(cy)}-{max(cy)} (all hindcast yrs; 1991-2020 unavailable)"
    clim_info[m]=cp
    if SPLIT and m in SPLIT_MODELS:
        c1=em.loc[[y for y in yrs if y<1999]].mean(); c2=em.loc[[y for y in yrs if 1999<=y<=2019]].mean()
        cser=pd.Series([c1 if y<1999 else c2 for y in yrs],index=yrs); cp=f"split 1982-1998 / 1999-2019 Sep-init years"; clim_info[m]=cp
    else:
        cser=pd.Series(em.loc[cy].mean(),index=yrs)
    for y in yrs: CL[(m,reg,sn,y)]=cser.loc[y]
    ga=g[g.year.isin(cy)]; sdm=(ga.prec-ga.year.map(cser)).std()
    for y in yrs:
        v=em.loc[y]; n=(g.year==y).sum(); c=cser.loc[y]
        mem=g[g.year==y].prec
        if reg=="nino34": out.append(dict(model=m,year=y,region=reg,season=sn,anom=v-c,n_mem=n))
        else: out.append(dict(model=m,year=y,region=reg,season=sn,pct_normal=100*v/c,z_member_sd=(v-c)/sdm,frac_members_above_normal=(mem>c).mean(),n_mem=n))
E=pd.DataFrame(out)
# member-level % of normal (primary regions) for noise / perfect-model diagnostics
Mm=M[M.region.isin(["SoCal_d6","NorCal_d2"])].copy()
Mm["clim"]=[CL[(a,b,c,d)] for a,b,c,d in zip(Mm.model,Mm.region,Mm.season,Mm.year)]
Mm["pct_normal"]=100*Mm.prec/Mm.clim
Mm[["model","year","member","region","season","pct_normal"]].to_csv(os.path.join(D,"nmme_member_pct_normal"+SUF+".csv"),index=False,float_format="%.1f")
n34=E[E.region=="nino34"][["model","year","anom"]].rename(columns={"anom":"nino34_NDJ_model"})
P=E[E.region!="nino34"].merge(n34,on=["model","year"],how="left")
obs=pd.read_csv(os.path.join(D,"obs_ca_winter_precip_enso.csv"))
obsmap={"SoCal_d6":"SoCal_d6","SoCal_box":"SoCal_d6","NorCal_d2":"NorCal_d2","NorCal_box":"NorCal_d2"}
P["obs_region"]=P.region.map(obsmap)
P=P.merge(obs[["decyear","season","region","pct_normal_9120","z_9120","ONI_NDJ","RONI_NDJ"]].rename(columns={"decyear":"year","region":"obs_region","pct_normal_9120":"obs_pct_normal","z_9120":"obs_z"}),on=["year","season","obs_region"],how="left")
P.to_csv(os.path.join(D,"nmme_sepinit_regional_series"+SUF+".csv"),index=False,float_format="%.3f")
pd.Series(clim_info).to_csv(os.path.join(D,"nmme_climatology_periods"+SUF+".csv"),header=["climatology_period"])
# ---- regressions
ost=pd.read_csv(os.path.join(D,"obs_regression_stats.csv"))
rows=[]
for (m,reg,sn),g in P[P.year<=2025].groupby(["model","region","season"]):
    g=g.dropna(subset=["nino34_NDJ_model"])
    if len(g)<10: continue
    lr=stats.linregress(g.nino34_NDJ_model,g.pct_normal); lz=stats.linregress(g.nino34_NDJ_model,g.z_member_sd)
    h=g.dropna(subset=["obs_pct_normal"])
    lo=stats.linregress(h.ONI_NDJ,h.obs_pct_normal)          # obs slope, same years as model
    lor=stats.linregress(h.RONI_NDJ,h.obs_pct_normal)
    n34r=np.corrcoef(h.nino34_NDJ_model,h.ONI_NDJ)[0,1]
    skill=np.corrcoef(h.pct_normal,h.obs_pct_normal)[0,1]
    o5025=ost[(ost.region==obsmap[reg])&(ost.season==sn)&(ost["index"]=="ONI_NDJ")&(ost.period=="1950-2025")].slope_pct_per_C.iloc[0]
    rows.append(dict(model=m,region=reg,season=sn,years=f"{g.year.min()}-{g.year.max()}",n=len(g),
        model_slope_pct_per_C=lr.slope,model_slope_se=lr.stderr,model_r=lr.rvalue,model_slope_z_per_C=lz.slope,
        obs_slope_ONI_sameyrs=lo.slope,obs_slope_ONI_sameyrs_se=lo.stderr,obs_slope_RONI_sameyrs=lor.slope,obs_slope_ONI_1950_2025=o5025,
        ratio_vs_obs_sameyrs=lr.slope/lo.slope,ratio_vs_obs_1950_2025=lr.slope/o5025,
        nino34_corr_model_vs_ONI=n34r,precip_skill_r=skill))
R=pd.DataFrame(rows); R.to_csv(os.path.join(D,"nmme_regression_vs_obs"+SUF+".csv"),index=False,float_format="%.3f")
pd.set_option("display.width",260); pd.set_option("display.max_columns",30)
for reg in ["SoCal_d6","NorCal_d2"]:
    print("\n==",reg); print(R[R.region==reg].drop(columns=["region"]).round(2).to_string(index=False))
for reg in ["SoCal_box","NorCal_box"]:
    print("\n== sensitivity",reg); print(R[R.region==reg][["model","season","model_slope_pct_per_C","obs_slope_ONI_sameyrs","ratio_vs_obs_sameyrs","precip_skill_r"]].round(2).to_string(index=False))
print("\nClimatology periods:"); print(pd.Series(clim_info).to_string())
# ---- events
ev=P[P.year.isin([1982,1997,2015,2023,2026])&P.region.isin(["SoCal_d6","NorCal_d2"])]
T=ev.pivot_table(index=["year","model"],columns=["region","season"],values="pct_normal").round(0)
T.columns=[f"{a}_{b}_pct" for a,b in T.columns]
T2=ev.drop_duplicates(["year","model"]).set_index(["year","model"])[["nino34_NDJ_model","ONI_NDJ","n_mem"]].round(2)
T=T2.join(T); T.to_csv(os.path.join(D,"nmme_event_table"+SUF+".csv"))
print("\nEvent table (% of each model's own normal; Nino3.4 NDJ model anomaly degC):"); print(T.to_string())
obsev=obs[obs.decyear.isin([1982,1997,2015,2023])&obs.region.isin(["SoCal_d6","NorCal_d2"])].pivot_table(index="decyear",columns=["region","season"],values="pct_normal_9120").round(0)
print("\nObserved (% of 1991-2020 normal):"); print(obsev.to_string())
f26=P[(P.year==2026)&P.region.isin(["SoCal_d6","NorCal_d2","SoCal_box","NorCal_box"])][["model","region","season","nino34_NDJ_model","pct_normal","z_member_sd","frac_members_above_normal","n_mem"]]
print("\n2026 Sep-init forecasts:"); print(f26.round(2).to_string(index=False))
f26.to_csv(os.path.join(D,"nmme_2026_sepinit_forecast"+SUF+".csv"),index=False,float_format="%.3f")

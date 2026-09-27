"""Observed CA climate-division precipitation vs NDJ ONI / RONI (1950-2025 winters)."""
import numpy as np, pandas as pd, os
H=os.path.join(os.path.dirname(__file__),".."); R=os.path.join(H,"raw"); D=os.path.join(H,"data")
# --- nClimDiv fixed width: SS DD EE YYYY + 12 x f7.2
rows=[]
for line in open(os.path.join(R,"climdiv-pcpndv.txt")):
    st,dv,el,yr=line[0:2],line[2:4],line[4:6],int(line[6:10])
    if st!="04" or el!="01": continue
    vals=[float(line[10+7*i:17+7*i]) for i in range(12)]
    rows.append([int(dv),yr]+vals)
df=pd.DataFrame(rows,columns=["div","year"]+list(range(1,13))).replace(-9.99,np.nan)
m=df.melt(id_vars=["div","year"],var_name="mon",value_name="p").pivot_table(index=["year","mon"],columns="div",values="p")
# area weights (km2, EPSG:5070 from NCEI CONUS_CLIMATE_DIVISIONS shapefile)
A={6:37536.,7:118191.,2:70766.}  # km2, EPSG:5070 areas of CA divs 6, 7, 2 from NCEI shapefile
m["SoCal_d6"]=m[6]; m["SoCal_d67"]=(m[6]*A[6]+m[7]*A[7])/(A[6]+A[7]); m["NorCal_d2"]=m[2]
m=m[["SoCal_d6","SoCal_d67","NorCal_d2"]]
def season(months, lab_offset):
    out={}
    for y in range(1949,2027):
        idx=[]
        for mo in months:
            yy = y if mo>=11 else y+1   # winter labelled by Dec year (ENSO year)
            idx.append((yy,mo))
        try: sub=m.loc[idx]
        except KeyError: continue
        if sub.isna().any().any() or len(sub)<3: continue
        out[y]=sub.sum()
    return pd.DataFrame(out).T
seas={"DJF":season([12,1,2],0),"JFM":season([1,2,3],0)}
# JFM labelled by preceding Dec year too (JFM 1998 -> 1997)
# --- ONI / RONI
def rd(fn,roni=False):
    t=pd.read_csv(os.path.join(R,fn),sep=r"\s+")
    t.columns=["SEAS","YR","ANOM"] if roni else ["SEAS","YR","TOTAL","ANOM"]
    return t[t.SEAS=="NDJ"].set_index("YR")["ANOM"]
oni=rd("oni.ascii.txt"); roni=rd("RONI.ascii.txt",True)
# validation: NDJ labelling; check NDJ 1997 sits between OND 1997 and DJF 1998
t=pd.read_csv(os.path.join(R,"oni.ascii.txt"),sep=r"\s+")
i=t.index[(t.SEAS=="NDJ")&(t.YR==1997)][0]
print("ONI order check:",t.loc[i-1,["SEAS","YR"]].tolist(),t.loc[i,["SEAS","YR","ANOM"]].tolist(),t.loc[i+1,["SEAS","YR"]].tolist())
print("Validation ONI NDJ 1997=%.2f (pub 2.4), NDJ 2015=%.2f (pub 2.6); RONI NDJ 1997=%.2f 2015=%.2f"%(oni[1997],oni[2015],roni[1997],roni[2015]))
yrs=range(1950,2026)
out=[]
for s,dd in seas.items():
    dd=dd.loc[[y for y in yrs if y in dd.index]]
    mons=[12,1,2] if s=="DJF" else [1,2,3]
    mclim=m.loc[1991:2020].groupby(level="mon").mean()   # 1991-2020 monthly means (NCEI convention)
    norm=mclim.loc[mons].sum()
    pct=100*dd/norm
    sd=dd.loc[1990:2019].std()  # interannual SD, winters Dec1990-Feb2020 ... (approx 1991-2020)
    z=(dd-norm)/sd
    for c in dd.columns:
        for y in dd.index:
            out.append(dict(winter=f"{y}-{str(y+1)[2:]}",decyear=y,season=s,region=c,precip_in=dd.loc[y,c],pct_normal_9120=pct.loc[y,c],z_9120=z.loc[y,c],ONI_NDJ=oni.get(y,np.nan),RONI_NDJ=roni.get(y,np.nan)))
obs=pd.DataFrame(out); obs.to_csv(os.path.join(D,"obs_ca_winter_precip_enso.csv"),index=False,float_format="%.3f")
mclim=m.loc[1991:2020].groupby(level="mon").mean()
print("1991-2020 normals (in) DJF:",mclim.loc[[12,1,2]].sum().round(2).to_dict()," JFM:",mclim.loc[[1,2,3]].sum().round(2).to_dict())
print("monthly normals div6 (J,F,M,D):",mclim.loc[[1,2,3,12],"SoCal_d6"].round(2).tolist(), " div2:",mclim.loc[[1,2,3,12],"NorCal_d2"].round(2).tolist())

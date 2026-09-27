import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, os
from scipy import stats
H=os.path.join(os.path.dirname(__file__),".."); D=os.path.join(H,"data")
obs=pd.read_csv(os.path.join(D,"obs_ca_winter_precip_enso.csv"))
P=pd.read_csv(os.path.join(D,"nmme_sepinit_regional_series.csv"))
SEASON="JFM"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":13,"axes.spines.top":False,"axes.spines.right":False})
INK="#0b0b0b"; INK2="#52514e"; MUTED="#9a9893"; OBS="#3d3d3a"; MOD="#2a78d6"; FC="#eb6834"
fig,axes=plt.subplots(1,2,figsize=(14,7.4),sharey=True)
LABOFF={"SoCal_d6":{1957:(-58,14),1965:(8,-4),1972:(6,-14),1982:(-62,4),1997:(6,6),2015:(8,-2),2023:(-30,12)},
        "NorCal_d2":{1957:(8,2),1965:(8,-4),1982:(-62,4),1997:(6,6),2015:(4,-18),2023:(-58,8),1991:(8,-4)}}
MOFF={"SoCal_d6":{"CanSIPS-IC4":(-78,8),"CESM1":(-14,12),"CCSM4":(10,-16),"CFSv2":(8,-4),"GEOSS2S":(-66,-4)},
      "NorCal_d2":{"CanSIPS-IC4":(-78,6),"CESM1":(4,8),"CCSM4":(-50,8),"CFSv2":(-38,-16),"GEOSS2S":(-38,-18)}}
for ax,(reg,title) in zip(axes,[("SoCal_d6","Southern California (South Coast Drainage, CA div. 6)"),("NorCal_d2","Northern California (Sacramento Drainage, CA div. 2)")]):
    o=obs[(obs.region==reg)&(obs.season==SEASON)].dropna(subset=["ONI_NDJ"])
    ax.axhline(100,color=MUTED,lw=1,zorder=0); ax.axvline(0,color=MUTED,lw=0.8,zorder=0)
    # model regression lines (ens-mean pct normal on own NDJ Nino3.4), drawn over each model's hindcast range
    g=P[(P.region==reg)&(P.season==SEASON)&(P.year<=2025)].dropna(subset=["nino34_NDJ_model"])
    for m,h in g.groupby("model"):
        lr=stats.linregress(h.nino34_NDJ_model,h.pct_normal); x0,x1=h.nino34_NDJ_model.min(),h.nino34_NDJ_model.max()
        xx=np.linspace(x0,x1,30); ax.plot(xx,lr.intercept+lr.slope*xx,color=MOD,lw=1.3,alpha=0.5,zorder=1)
        xx=np.linspace(x1,4.8,20); ax.plot(xx,lr.intercept+lr.slope*xx,color=MOD,lw=1.1,alpha=0.45,ls=(0,(1.5,2)),zorder=1)
        if m=="CMC1-CanCM3" and reg=="SoCal_d6": ax.annotate("CanCM3 (retired)",(2.6,lr.intercept+lr.slope*2.6),xytext=(0,-14),textcoords="offset points",fontsize=9.5,color=MOD)
    lo=stats.linregress(o.ONI_NDJ,o.pct_normal_9120); xx=np.linspace(o.ONI_NDJ.min(),o.ONI_NDJ.max(),50)
    ax.plot(xx,lo.intercept+lo.slope*xx,color=INK,lw=2.6,zorder=3)
    xx=np.linspace(o.ONI_NDJ.max(),4.8,20); ax.plot(xx,lo.intercept+lo.slope*xx,color=INK,lw=2.0,ls=(0,(2,2)),zorder=3)
    ax.axvspan(o.ONI_NDJ.max(),4.9,color="#f3f2ee",zorder=-1)
    ax.text(o.ONI_NDJ.max()+0.08,6,"beyond observed\nrange",fontsize=10,color=INK2,va="bottom")
    ax.scatter(o.ONI_NDJ,o.pct_normal_9120,s=46,color=OBS,edgecolor="white",lw=1,zorder=4)
    OFF=LABOFF[reg]
    for r in o[o.decyear.isin(OFF.keys())].itertuples():
        ax.annotate(f"{r.decyear}–{str(r.decyear+1)[2:]}",(r.ONI_NDJ,r.pct_normal_9120),xytext=OFF[r.decyear],textcoords="offset points",fontsize=10.5,color=INK2,zorder=5,
                    arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.7,shrinkA=0,shrinkB=3))
    f=P[(P.region==reg)&(P.season==SEASON)&(P.year==2026)].dropna(subset=["nino34_NDJ_model"])
    ax.scatter(f.nino34_NDJ_model,f.pct_normal,s=120,marker="D",color=FC,edgecolor="white",lw=1.2,zorder=6)
    for r in f.itertuples():
        nm=r.model.replace("COLA-RSMAS-","").replace("NCEP-","").replace("NASA-","")
        ax.annotate(nm.replace("GEOSS2S","GEOS-S2S"),(r.nino34_NDJ_model,r.pct_normal),xytext=MOFF[reg][nm],textcoords="offset points",fontsize=10,color=INK2,zorder=7)
    ax.set_title(title,fontsize=13.5,loc="left",color=INK,pad=26)
    ax.set_xlabel("Nov–Jan Niño-3.4 anomaly (°C)\nobs: CPC ONI (ERSSTv5, 30-yr centred base) · models: own 1991–2020 clim.",fontsize=11.5,color=INK2)
    ax.set_xlim(-2.3,4.9); ax.grid(axis="y",color="#e6e5e0",lw=0.8); ax.set_axisbelow(True)
    ax.text(0.0,1.015,f"Observed slope {lo.slope:+.0f} pp per °C, r = {lo.rvalue:.2f} (1950–2025)",transform=ax.transAxes,fontsize=11,color=INK2,va="bottom")
axes[0].set_ylabel(f"{SEASON} precipitation (% of 1991–2020 normal)",fontsize=12.5,color=INK2)
axes[0].set_ylim(0,max(260,axes[0].get_ylim()[1]))
from matplotlib.lines import Line2D
hs=[Line2D([],[],marker="o",ls="",color=OBS,markersize=7,label="Observed winters 1950–51 to 2025–26 (NOAA nClimDiv)"),
    Line2D([],[],color=INK,lw=2.6,label="Observed linear fit"),
    Line2D([],[],color=MOD,lw=1.3,alpha=0.6,label="NMME Sept-start hindcast fits, one per model (dotted = extrapolated)"),
    Line2D([],[],marker="D",ls="",color=FC,markersize=9,label="Sept 2026 real-time forecasts (ensemble mean)")]
fig.legend(handles=hs,loc="lower center",ncol=2,frameon=False,fontsize=11.5,bbox_to_anchor=(0.5,0.0))
omax=obs.ONI_NDJ.max(); f26=P[(P.year==2026)].dropna(subset=["nino34_NDJ_model"]).drop_duplicates("model")
fig.suptitle(f"Every Sept 2026 model forecast sits beyond the strongest observed El Niño (ONI {omax:.1f} °C)",x=0.01,ha="left",y=0.975,fontsize=16.5,fontweight="bold",color=INK)
fig.text(0.01,0.905,f"Jan–Mar precipitation vs Nov–Jan Niño-3.4. Model hindcast fits (1980s–2025) roughly match the observed slope in the south; 2026 values are extrapolation.",fontsize=12,color=INK2,ha="left")
fig.subplots_adjust(left=0.065,right=0.985,top=0.80,bottom=0.205,wspace=0.07)
fig.savefig(os.path.join(H,"fig_ca_precip_vs_nino34_nmme.png"),dpi=150)
print("saved")

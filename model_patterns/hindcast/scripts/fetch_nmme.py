"""Fetch NMME Sep-initialised hindcasts/forecasts from IRI/LDEO Data Library via OPeNDAP.
Precip: all members, 1-deg cells in box 32-42N, 235-246E (125-114W), leads 2.5..6.5 (Nov..Mar for S=Sep).
SST: Nino3.4 area average computed server-side (Ingrid [X Y]average), all members, leads 0.5..6.5.
Output: data/nmme_raw/<model>_<stream>_{prec,nino34}.nc (small)."""
import xarray as xr, numpy as np, os, sys, time
B="https://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME"
OUT=os.path.join(os.path.dirname(__file__),"..","data","nmme_raw"); os.makedirs(OUT,exist_ok=True)
STREAMS={
 "NCEP-CFSv2":["HINDCAST/.MONTHLY","FORECAST/.EARLY_MONTH_SAMPLES/.MONTHLY"],
 "CanSIPS-IC4":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "CanSIPS-IC3":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "CanSIPSv2":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "NASA-GEOSS2S":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "COLA-RSMAS-CCSM4":["MONTHLY"],
 "COLA-RSMAS-CESM1":["MONTHLY"],
 "GFDL-SPEAR":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "NCAR-CESM1":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "CMC1-CanCM3":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
 "CMC2-CanCM4":["HINDCAST/.MONTHLY","FORECAST/.MONTHLY"],
}
def sep_slice(S):
    mon=np.round(S).astype(int)%12  # 8 = Sep
    idx=np.where(mon==8)[0]
    if len(idx)==0: return None
    if len(idx)>1: assert np.all(np.diff(idx)==12), "non-contiguous S"
    return slice(idx[0],idx[-1]+1,12)
def get(url,sel,tries=4):
    for k in range(tries):
        try:
            ds=xr.open_dataset(url,decode_times=False)
            return ds
        except Exception as e:
            print("retry",k,url[-80:],str(e)[:80]); time.sleep(10)
    raise RuntimeError(url)
models=sys.argv[1:] or list(STREAMS)
for m in models:
    for st in STREAMS[m]:
        tag=f"{m}_{st.split('/')[0]}"
        fp=os.path.join(OUT,tag+"_prec.nc"); fs=os.path.join(OUT,tag+"_nino34.nc")
        try:
            if not os.path.exists(fp):
                ds=get(f"{B}/.{m}/.{st}/.prec/dods",None)
                sl=sep_slice(ds.S.values)
                if sl is None: print(tag,"no Sep starts"); continue
                L=ds.L.values; li=np.where((L>=2.4)&(L<=6.6))[0]
                da=ds.prec.isel(S=sl,L=slice(li[0],li[-1]+1)).sel(Y=slice(32,42),X=slice(235,246)).load()
                da.to_netcdf(fp); print(tag,"prec",dict(da.sizes),float(1960+da.S.min()/12),float(1960+da.S.max()/12),flush=True)
            if not os.path.exists(fs):
                u=f"{B}/.{m}/.{st}/.sst/X/190/240/RANGEEDGES/Y/-5/5/RANGEEDGES/%5BX/Y%5Daverage/dods"
                ds=get(u,None)
                sl=sep_slice(ds.S.values)
                if sl is None: print(tag,"no Sep sst"); continue
                da=ds.sst.isel(S=sl).sel(L=slice(0.4,6.6)).load()
                da.to_netcdf(fs); print(tag,"sst",dict(da.sizes),flush=True)
        except Exception as e:
            print(tag,"FAILED",str(e)[:200],flush=True)

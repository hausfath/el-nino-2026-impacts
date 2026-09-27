"""Area weights of NMME 1-deg cells (centres at integer lon/lat, +/-0.5) for model regions:
 SoCal_d6 : overlap with CA climate division 6 (South Coast Drainage)  [primary]
 NorCal_d2: overlap with CA climate division 2 (Sacramento Drainage)    [primary]
 SoCal_box: 32.5-35N, 121-114.5W intersected with California land       [sensitivity, task-specified box]
 NorCal_box: 38-41.5N, 123-120W intersected with California land        [sensitivity]
weight = overlap area (equal-area CRS EPSG:5070)."""
import geopandas as gpd, numpy as np, pandas as pd, os
from shapely.geometry import box
H=os.path.join(os.path.dirname(__file__),"..")
g=gpd.read_file(os.path.join(H,"raw/shp/GIS.OFFICIAL_CLIM_DIVISIONS.shp"))
ca=g[g.STATE=="California"]
d6=ca[ca.CD_NEW==6].to_crs(5070).union_all(); d2=ca[ca.CD_NEW==2].to_crs(5070).union_all()
caall=ca.to_crs(5070).union_all()
def tobox(x0,x1,y0,y1): return gpd.GeoSeries([box(x0,y0,x1,y1)],crs=4326).to_crs(5070).iloc[0]
sbox=tobox(-121,-114.5,32.5,35).intersection(caall); nbox=tobox(-123,-120,38,41.5).intersection(caall)
rows=[]
for lat in range(32,43):
    for lon in range(235,247):
        c=tobox(lon-360-0.5,lon-360+0.5,lat-0.5,lat+0.5)
        rows.append(dict(Y=lat,X=lon,SoCal_d6=c.intersection(d6).area/1e6,NorCal_d2=c.intersection(d2).area/1e6,
                         SoCal_box=c.intersection(sbox).area/1e6,NorCal_box=c.intersection(nbox).area/1e6,cell_km2=c.area/1e6))
w=pd.DataFrame(rows); w.to_csv(os.path.join(H,"data/model_region_weights.csv"),index=False,float_format="%.1f")
for r in ["SoCal_d6","NorCal_d2","SoCal_box","NorCal_box"]:
    s=w[w[r]>0]; print(r,"cells",len(s),"total km2 %.0f"%s[r].sum()); print(s.pivot(index="Y",columns="X",values=r).div(s.cell_km2.mean()).round(2).fillna(0).iloc[::-1].to_string())

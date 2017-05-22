import pandas
import numpy as np

import geopandas

from simpledbf import Dbf5
import pandas_access as mdb

# Parcel Shape file
prcl_shp = geopandas.GeoDataFrame.from_file('data/open-data-extracted/prcl_shape/prcl.shp')

# Join Parcel Info
Prcl =  mdb.read_table("data/open-data-extracted/prcl/prcl.mdb", "Prcl")
parcels = pandas.merge(prcl_shp,Prcl,left_on='HANDLE',right_on='Handle')
parcels.loc[:,'Nbrhd']= parcels.Nbrhd.astype(int)

# Join in Neighborhood names
neighborhoods = geopandas.read_file('data/open-data-extracted/nbrhds_wards/BND_Nhd88_cw.shp')
parcels = pandas.merge(parcels,neighborhoods[['NHD_NAME','NHD_NUM']],left_on='Nbrhd',right_on='NHD_NUM')

# Join More Parcel info, this one has nice address names to join to CSB data
par = Dbf5('data/open-data-extracted/par/par.dbf',codec='cp1250').to_dataframe()
parcels = pandas.merge(parcels,par,on='HANDLE')

parcels.loc[:,'parcel_address'] = parcels.SITEADDR.apply(lambda x: x.replace(' AV','').replace(' ST','').replace(' DR','').replace(' BLVD','').replace('   ',''))

parcels= parcels[[   'HANDLE',
                     'geometry',
                     'CityBlock',
                     'OwnerCode',
                     'AddrType',
                     'LowAddrNum',
                     'LowAddrSuf',
                     'HighAddrNum',
                     'HighAddrSuf',
                     'NLC',
                     'Parity',
                     'StPreDir',
                     'StName',
                     'StType',
                     'StSufDir',
                     'StdUnitNum',
                     'OwnerName',
                     'OwnerName2',
                     'OwnerAddr',
                     'OwnerCity',
                     'OwnerState',
                     'OwnerCountry',
                     'OwnerZIP',
                     'VacantLot',
                     'Condominium',
                     'NbrOfUnits',
                     'NbrOfApts',
                     'Frontage',
                     'LandArea',
                     'VacBldgYear',
                     'GeoCityBlockPart',
                     'Ward10',
                     'Precinct10',
                     'InspArea10',
                     'CDADist',
                     'CDASubDist',
                     'PoliceDist',
                     'CensTract10',
                     'CensBlock10',
                     'HouseConsDist',
                     'OwnerOcc',
                     'OwnerUpdate',
                     'NHD_NAME',
                     'NHD_NUM',
                     'SITEADDR',
                     'parcel_address']]

parcels.to_crs( "+init=epsg:4326",inplace=True)
parcels.loc[:,'geometry_centroid'] = parcels.centroid
parcels.loc[:,'lon'] = parcels.geometry.centroid.apply(lambda x: x.x)
parcels.loc[:,'lat'] = parcels.geometry.centroid.apply(lambda x: x.y)
parcels.loc[:,'url'] = parcels.HANDLE.apply(lambda x: 'http://dynamic.stlouis-mo.gov/citydata/newdesign/data.cfm?Handle=' + str(x))


del prcl_shp
del Prcl
del par
del neighborhoods

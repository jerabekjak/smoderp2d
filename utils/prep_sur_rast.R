library('raster')
r0 = raster('/home/hdd/data/2019_COST-experiment/gisdata/uhor_pred.tif')
r0fill = raster('/home/hdd/data/2019_COST-experiment/gisdata/uhor_pred_fill.tif')
mask = shapefile('/home/hdd/data/2019_COST-experiment/gisdata/clip_uhor.shp')

ret = (r0 - r0fill)

crop_ = crop(ret, mask)
r0out = mask(crop_, mask)
plot(r0out)

writeRaster(x = r0out, filename = 'tests/data/reten.asc')

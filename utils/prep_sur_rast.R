library('raster')
r0 = raster('/home/hdd/data/2019_COST-experiment/gisdata/uhor_pred.tif')
r0fill = raster('/home/hdd/data/2019_COST-experiment/gisdata/uhor_pred_fill.tif')
mask = shapefile('/home/hdd/data/2019_COST-experiment/gisdata/clip_uhor.shp')

ret = (r0 - r0fill)

crop_ = crop(ret, mask)
r0out = mask(crop_, mask)
r0outarg = raster::aggregate(r0out, fact = 5, fun = min)
r0outargnozero = r0outarg
values(r0outargnozero)[values(r0outargnozero) == 0] = NA
plot(r0outargnozero)
plot(r0outarg)


writeRaster(x = r0outarg, filename = 'tests/data/reten.asc', overwrite = TRUE)

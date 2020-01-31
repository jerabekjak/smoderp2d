# root dir
root  <-  "~/Documents/Smoderp/smoderp2d-fork"
# output dir
outdir <- 'tests/data/output/'
# choose points to be printed (*.dat file v output dir)
dx = 0.05

#
#
# Main
#
dir_ = paste(root, outdir, sep='/')
sep_  = ';'
skip_ = 3
extension_ = '*.dat'

files  = c()
for (idir_ in dir_) {
  files = c(files,list.files(idir_,pattern = '*.dat',full.names = TRUE))
}



#pixel = read.table(paste(files[1],sep = ''),skip=2,nrows = 1,comment.char = '')
#print (pixel)
#pixel = as.numeric(pixel[2])
#pixel = 
H = list()
for (file_ in files) {
  name_ = substr(file_,1,8)
  name_ = file_
  print (name_)
  H[[name_]] = read.table(file_,sep = sep_, header = F,skip=skip_+1, comment.char = '')
}


runoff = rep(0, length(H[[1]][,1]))
xxx = 0
for (h in H){
  
  runoff = runoff + h$V5
  yyy = range(xxx, h$V5)
}
# 
# print (runoff)
layout(matrix(c(1,2), ncol = 2))
par(mar=c(4,4,1,1))
xx = range(runoff*100*60*60)
yy = range(h$V1/60/60)
plot(NA, xlim = yy, ylim = xx, ylab = 'runoff [mm/h]', xlab = 'time [h]')
for (h in H){
  lines(h$V1/60/60, h$V5*100*60*60, type = 'b', cex=0.2) 
}

plot(h$V1/60/60,runoff*100*60*60, ylab = 'runoff [mm/h]', xlab = 'time [h]', cex=0.2)

asdf
layout(matrix(c(1), ncol = 1))
library('fields')
r = t(as.matrix(read.table('../tests/data/output/prubeh/H000000000010_00.asc')))
par(mar=c(1,1,1,4))
image.plot(r, axes=F, main = 'surface retention [m]')
r = t(as.matrix(read.table('../tests/data/output/prubeh/H000000003604_26.asc')))
image.plot(r, axes=F, main = 'surface retention [m]')

# xx = c()
# yy = c()
# for (h in H){
#   xx = range(xx, h$V1, na.rm = T)
#   yy = range(yy, h$V5, na.rm = T)
# }
# plot(NA, xlim=xx, ylim=yy)
# for (h in H){
#   lines(h$V1, h$V5)
# }

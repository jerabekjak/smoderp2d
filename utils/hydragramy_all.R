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
#pixel = H = list()
for (file_ in files) {
  name_ = substr(file_,1,8)
  name_ = file_
  print (name_)
  H[[name_]] = read.table(file_,sep = sep_, header = F,skip=skip_+1, comment.char = '')
}

runoff = rep(0, length(H[[1]][,1]))
for (h in H){
  runoff = runoff + h$V5
}

print (runoff)
plot(h$V1,runoff)

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

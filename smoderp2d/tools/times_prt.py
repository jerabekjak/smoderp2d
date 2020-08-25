import numpy as np
import os
from smoderp2d.core.general import *
from smoderp2d.providers import Logger

from smoderp2d.core.general import Globals
from smoderp2d.providers.cmd import CmdWritter


class TimesPrt(object):
    def __init__(self):
        if not Globals.prtTimes:
            self.fTimes = None
            return

        self.fTimes = open(Globals.prtTimes, 'r')
        self.outsubrid = 'prubeh'
        os.makedirs(os.path.join(Globals.outdir, self.outsubrid))
        self.writer = CmdWritter().write_raster

        self.times = []
        self.__n = 0

        for line in self.fTimes.readlines():
            z = line.split()
            if len(z) == 0:
                continue
            elif z[0].find('#') >= 0:
                continue
            else:
                if len(z) == 0:
                    continue
                else:
                    self.times.append(float(line) * 60.0)
        self.times.sort()

    def prt(self, time, dt, sur):
        if not self.fTimes:
            return
        
        #Logger.info('-----------------debugLogger.info{}'.format(__file__))
        #Logger.info('self.__n: {}'.format(self.__n))
        #Logger.info('len(self.times): {}'.format(len(self.times)))
        if self.__n == len(self.times):
            return

        #Logger.info('time: {}'.format(time))
        #Logger.info('self.times[self.__n]: {}'.format(self.times[self.__n]))
        #Logger.info('time+dt: {}'.format(time+dt))
        #Logger.info('end--------------debugLogger.info{}'.format(__file__))
        if (time <= self.times[self.__n]) and (self.times[self.__n] < time+dt):

            cas = '%015.2f' % (time + dt)
            dirin = os.path.join(Globals.outdir,
                                  self.outsubrid)
            filein = 'r' + str(cas).replace('.', '_') + 'reten'
            filein_hnew = 'r' + str(cas).replace('.', '_') + 'h_new'
            Logger.info("Printing total H into file {}/{}".format(dirin,filein))
            tmp = np.zeros([GridGlobals.r, GridGlobals.c], float)
            tmp_hnew = np.zeros([GridGlobals.r, GridGlobals.c], float)

            for i in GridGlobals.rr:
                for j in GridGlobals.rc[i]:
                    tmp[i][j] = sur.arr[i][j].sur_ret
                    tmp_hnew[i][j] = sur.arr[i][j].h_total_new

            self.writer(tmp, filein, dirin)
            self.writer(tmp_hnew, filein_hnew, dirin)

            # pro pripat, ze v dt by bylo vice pozadovanych tisku, v takovem pripade udela jen jeden
            # a skoci prvni cas, ktery je mimo
            while (time <= self.times[self.__n]) and (self.times[self.__n] < time+dt):
                self.__n += 1
                if self.__n == len(self.times):
                    return

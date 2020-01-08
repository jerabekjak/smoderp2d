import os
import sys
import math
import argparse
import logging
import numpy as np
if sys.version_info.major >= 3:
    from configparser import ConfigParser, NoSectionError
else:
    from ConfigParser import ConfigParser, NoSectionError

from smoderp2d.core.general import Globals, GridGlobals, DataGlobals
from smoderp2d.providers.base import BaseProvider, Logger, CompType, BaseWritter
from smoderp2d.exceptions import ConfigError

class CmdWritter(BaseWritter):
    def __init__(self):
        super(CmdWritter, self).__init__()

    def write_raster(self, array, output_name, directory='core'):
        """Write raster (numpy array) to ASCII file.

        :param array: numpy array
        :param output_name: output filename
        :param directory: directory where to write output file
        """
        file_output = self._raster_output_path(output_name, directory)

        np.savetxt(file_output, array, fmt='%.3e')

        self._print_array_stats(
            array, file_output
        )

class NoGISProvider(BaseProvider):
    def __init__(self):
        """Create argument parser."""
        super(NoGISProvider, self).__init__()
        
        # define CLI parser
        parser = argparse.ArgumentParser(description='Run Smoderp2D.')

        # type of computation
        parser.add_argument(
            '--typecomp',
            help='type of computation',
            type=str,
            choices=['full',
                     'dpre',
                     'roff'],
            required=True
        )

        # data file (only required for runoff)
        parser.add_argument(
            '--indata',
            help='file with prepared data',
            type=str
        )
        self.args = parser.parse_args()
        self.args.typecomp = CompType()[self.args.typecomp]

        # load configuration
        self._config = ConfigParser()
        if self.args.typecomp == CompType.roff:
            if not self.args.indata:
                parser.error('--indata required')
            if not os.path.exists(self.args.indata):
                raise ConfigError("{} does not exist".format(
                    self.args.indata
                ))
            self._config.read(self.args.indata)

        try:
            # set logging level
            Logger.setLevel(self._config.get('Other', 'logging'))
            # sys.stderr logging
            self._add_logging_handler(
                logging.StreamHandler(stream=sys.stderr)
            )

            # must be defined for _cleanup() method
            Globals.outdir = self._config.get('Other', 'outdir')
        except NoSectionError as e:
            raise ConfigError('Config file {}: {}'.format(
                self.args.indata, e
            ))

        self._sklon = self._config.getfloat('params','sklon')
        self._hcrit = self._config.getfloat('params','hcrit')
        self._X = self._config.getfloat('params','X')
        self._Y = self._config.getfloat('params','Y')
        self._b = self._config.getfloat('params','b')
        self._Ks = self._config.getfloat('params','Ks')
        self._S = self._config.getfloat('params','S')
        self._ppl = self._config.getfloat('params','ppl')
        self._pi = self._config.getfloat('params','pi')
        self._n = self._config.getfloat('params','n')


        # TODO dej vse do globals
        self._r = self._config.getint('matrices','r')
        self._c = self._config.getint('matrices','c')
        self._pixel_area = self._config.getfloat('matrices','pixel_area')

        self._sur_ret_mu = self._config.getfloat('reten','mu')
        self._sur_ret_sigma = self._config.getfloat('reten','sigma')


        # define storage writter
        self.storage = CmdWritter()

        print ('')
        print ('')
        print ('NO GIS PROVIDER')
        print ('')
        print ('')
        print ('')

    def load(self):
        """Load configuration data.

        Only roff procedure supported.
        """
        if self.args.typecomp == CompType.roff:
            # cleanup output directory first
            self._cleanup()

            data = self._load_roff(
                self._config.get('Other', 'indata')
            )


            # # TODO
            # combinatIndex
            # points

            # # TODO coto ?
            # poradi
            # c

            # # TODO i toto?
            # yllcorner
            # xllcorner

            # print (data['mat_fd'])
            # for key in data.keys(): 
            #     print (key)

            # from base provider class call
            self._set_globals(data)
            self._set_grid_globals()
            self._resize_matrices()
            self._set_matrices()

            self._set_philips_to_glob()
            self._set_surface_retention()

        else:
            raise ProviderError('Unsupported partial computing: {}'.format(
                self.args.typecomp
            ))


    def _set_grid_globals(self):
        # # TODO co toto?
        # vpix
        # spix
        r = self._r
        c = self._c
        pa = self._pixel_area
        rr = (range(2,(r-1)))
        rc = [[]]*r
        for i in rr:
            rc[i] = range(2,(c-1))
        dx = math.sqrt(pa)
        dy = dx

        GridGlobals.r = r
        GridGlobals.c = c
        GridGlobals.rr = rr
        GridGlobals.rc = rc
        GridGlobals.pixel_area = pa
        GridGlobals.dx = dx
        GridGlobals.dy = dy

    def _resize_matrices(self):
        # TODO
        # array_points mozna
        r = self._r
        c = self._c
        
        Globals.mat_b = np.full((r, c), np.nan)
        Globals.mat_n = np.full((r, c), np.nan)
        Globals.mat_inf_index = np.full((r, c), np.nan)
        Globals.mat_fd = np.full((r, c), np.nan)
        Globals.mat_hcrit = np.full((r, c), np.nan)
        DataGlobals.mat_ppl = np.full((r, c), np.nan)
        Globals.mat_aa = np.full((r, c), np.nan)
        Globals.mat_reten = np.full((r, c), np.nan)
        Globals.mat_nan = np.full((r, c), np.nan)
        Globals.mat_efect_cont = np.full((r, c), np.nan)
        Globals.mat_pi = np.full((r, c), np.nan)
        Globals.mat_slope = np.full((r, c), np.nan)
        Globals.mat_dem = np.full((r, c), np.nan)
        Globals.mat_boundary = np.full((r, c), np.nan)

    def _set_matrices(self):
        
        Globals.mat_slope.fill(self._sklon)
        X = self._X
        Y = self._Y
        Globals.mat_aa = X*Globals.mat_slope**Y
        Globals.mat_b.fill(self._b)
        Globals.mat_n.fill(self._n)
        Globals.mat_inf_index.fill(1)
        Globals.mat_fd.fill(4)
        Globals.mat_hcrit.fill(self._hcrit)
        DataGlobals.mat_ppl.fill(self._ppl)
        Globals.mat_nan.fill(np.nan)
        Globals.mat_efect_cont.fill(GridGlobals.dx)
        Globals.mat_pi.fill(self._pi)
        # Globals.mat_dem = np.full((r, c), np.nan)
        # Globals.mat_boundary = np.full((r, c), np.nan)


    def _set_surface_retention(self):
        mu, sigma = self._sur_ret_mu, self._sur_ret_sigma # mean and standard deviation
        mat_reten = Globals.mat_reten.astype(float)
        dim = mat_reten.shape
        n = dim[0]
        m = dim[1]
        for i in range(n):
            for j in range(m):
                mat_reten[i][j] = abs(np.random.normal(mu, sigma, 1))
        Globals.mat_reten = -mat_reten

    def _set_philips_to_glob(self):
        """ read philip paramaters from hidden file """
        ks = self._Ks
        s = self._S

        for l in Globals.combinatIndex:
            l[1] = ks
            l[2] = s


    

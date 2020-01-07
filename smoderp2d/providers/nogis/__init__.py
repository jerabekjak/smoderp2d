import os
import sys
import argparse
import logging
import numpy as np
if sys.version_info.major >= 3:
    from configparser import ConfigParser, NoSectionError
else:
    from ConfigParser import ConfigParser, NoSectionError

from smoderp2d.core.general import Globals
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

        self._sklon = self._config.getfloat('sklon-hcrit','sklon')
        self._hcrit = self._config.getfloat('sklon-hcrit','hcrit')
        self._X = self._config.getfloat('sklon-hcrit','X')
        self._Y = self._config.getfloat('sklon-hcrit','Y')
        self._b = self._config.getfloat('sklon-hcrit','b')
        self._Ks = self._config.getfloat('sklon-hcrit','Ks')
        self._S = self._config.getfloat('sklon-hcrit','S')


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

            self._set_globals(data)

            self._set_surface_retention(data['mat_reten'])
            self._set_philips_to_glob()
            self._set_slope_to_glob() 
            self._set_optim_params_to_glob()
        else:
            raise ProviderError('Unsupported partial computing: {}'.format(
                self.args.typecomp
            ))



    def _set_surface_retention(self, mat_reten):
        mu, sigma = 0.001, 0.0001 # mean and standard deviation
        mat_reten = mat_reten.astype(float)
        dim = mat_reten.shape
        n = dim[0]
        m = dim[1]
        print (mat_reten)
        for i in range(n):
            for j in range(m):
                mat_reten[i][j] = np.random.normal(mu, sigma, 1)
        print (mat_reten)
        raw_input()
        Globals.mat_reten = -mat_reten

    def _set_philips_to_glob(self):
        """ read philip paramaters from hidden file """
        ks = self._Ks
        s = self._S

        for l in Globals.combinatIndex:
            l[1] = ks
            l[2] = s

    def _set_slope_to_glob(self):
        """ change surface slope in globals.mat_slope """
        Globals.mat_slope.fill(self._sklon)

    def _set_optim_params_to_glob(self):
        """ change surface slope in globals.mat_aa a globals.mat_aa """
        X = self._X
        Y = self._Y
        b = self._b

        Globals.mat_aa = X*Globals.mat_slope**Y
        Globals.mat_b.fill(b)

    

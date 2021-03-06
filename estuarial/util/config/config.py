import os
import six
from os.path import dirname
from os.path import join as pjoin
from six.moves import configparser

# If running in Google App Engine there is no "user" and
# os.path.expanduser() will fail. Attempt to detect this case and use a
# no-op expanduser function in this case.
try:
  os.path.expanduser('~')
  expanduser = os.path.expanduser
except (AttributeError, ImportError):
  # This is probably running on App Engine.
  expanduser = (lambda x: x)

# By default we use two locations for the estuarial configurations,
# /etc/odbc.ini and ~/.estuarial/estuarial.ini (which works on Windows and Unix).

EstuarialConfigPath = pjoin(dirname(__file__), 'estuarial.ini')
EstuarialConfigLocations = [EstuarialConfigPath]
UserConfigPath = pjoin(expanduser('~'), '.estuarial', 'estuarial.ini')
UserConfigDir = pjoin(expanduser('~'), '.estuarial')
EstuarialConfigLocations.insert(0, UserConfigPath)

class Config(configparser.SafeConfigParser):

    def __init__(self, path=None,):
        if six.PY3:
            super(Config, self).__init__(allow_no_value=True)
        else:
            # We don't use ``super`` here, because ``ConfigParser`` still uses
            # old-style classes.
            configparser.SafeConfigParser.__init__(self, allow_no_value=True)

        if path:
            self.read(path)
            self.file_path = path
        else:
            f = self.read(EstuarialConfigLocations)
            self.file_path = f[0]

    def get(self, section, name, default=None):
        try:
            val = configparser.SafeConfigParser.get(self, section, name)
        except:
            val = default
        return val

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

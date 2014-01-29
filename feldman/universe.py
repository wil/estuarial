from __future__ import print_function, division, absolute_import

from sqlalchemy.sql import column, and_, or_
import datetime as dt
from feldman.arraymanagementclient import ArrayManagementClient
import feldman.indexing as indexing

class Universe(ArrayManagementClient):
    """
    universe object
    """

    def __init__(self,DataFrame):
        super(Universe, self).__init__()
        self.data = DataFrame

    def __repr__(self):
        return ("TR Universe")

    def __str__(self):
        return ("TR Universe")

    @classmethod
    def _create_metrics(cls, name, metric_class):
        """
        fancy method of instantiating object

        """

        if getattr(cls, name, None) is None:
            underscore_name = '_%s' % name
            setattr(cls, underscore_name, None)

            def _metric_loader(self):
                i = getattr(self, underscore_name)
                if i is None:
                    i = metric_class(self, name)
                    setattr(self, underscore_name, i)
                return i

            setattr(cls, name, property(_metric_loader))


for _name, _metric_class in indexing.get_metrics_list():
    Universe._create_metrics(_name, _metric_class)

from feldman.arraymanagementclient import ArrayManagementClient
from sqlalchemy.sql import column, and_, or_


'''
influenced heavily by pandas
'''

# the supported metrics
def get_metrics_list():

    return [
        ('ohlc', _OHLCIndexer),
        ('cash', _CASHIndexer),
    ]

class _TRUniverseIndexer(ArrayManagementClient):

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name


    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            print("index is a slice")
            return start, stop

        else:
            raise TypeError("index must be datetime slice")



class _OHLCIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            print("index is a slice")

            universe = self.obj.data.seccode.tolist()
            arr = self.obj.aclient['/DataStream/ohlc.fsql']
            ohlc = arr.select(and_(arr.seccode.in_(universe),arr.marketdate >= start, \
                                arr.marketdate <= stop))

            return ohlc
        else:
            raise TypeError("index must be datetime slice")

class _CASHIndexer(_TRUniverseIndexer):

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start
            stop = index.stop
            print("index is a slice")

            universe = self.obj.data.seccode.tolist()
            item = 2001 #cash
            freq = 'Q' #Quarterly Maybe use step for this?
            arr = self.obj.aclient['/WORLDSCOPE/worldscope_metrics_date_select.fsql']

            cash = arr.select(and_(arr.seccode.in_(universe),
                                    arr.item==item,
                                    arr.freq==freq,
                                    arr.fdate >=start,
                                    arr.fdate >=stop
                                  )
                             )
            return cash
        else:
            raise TypeError("index must be datetime slice")







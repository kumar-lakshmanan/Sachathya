#For Sachathya

import numpy as np
import pyqtgraph as pg

data = np.random.normal(size=1000)
#data = [5,8,4,1,9,7,3,6,2,10]
print(data)
pg.plot(data, title="Simplest possible plotting example")
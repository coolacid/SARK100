#!/usr/bin/env python3
from pysark100 import sark100

s = sark100()

data = s.scan_band("40m", buffer_pct=0.10, step=10000, progress=True)
# data = s.scan_band("hf", buffer_pct=0, step=10000, progress=True)

#for x in data:
#    print(x)

print(data.get_dataframe())
data.plot(show_bands=True)
data.plot_interactive()

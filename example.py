#!/usr/bin/env python3
from pysark100 import sark100

s = sark100()

data = list(s.scan_band("40m", buffer_pct=0.10, step=10000, progress=True))
# data = list(s.scan_band("hf", buffer_pct=0, step=10000, progress=True))
print(s.data.get_data())
s.data.plot(show_bands=True)
s.data.plot_interactive()

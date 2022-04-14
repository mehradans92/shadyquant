# shadyquant

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/whitead/shadyquant)
[![PyPI version](https://badge.fury.io/py/shadyquant.svg)](https://badge.fury.io/py/shadyquant)

This python package allows you to quantile and plot lines where you have multiple samples, typically for visualizing uncertainty.  Your data should be shaped `(N, T)`, where `N` is the number of
samples, `T` is the dimension of your lines.

## Install

```sh
pip install shadyquant
```

## Example

Consider you have 100 lines that you want to compute confidence intervals (quantiles) on:

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2,1000)
y = np.sin(x)
plt.plot(x,y)

w = np.random.normal(size=100)**2
traj = y + y * w[:, None]
plt.plot(traj.T, color='C0')
plt.show()
```

You can use shadyquant to plot a 95% confidence interval:

```py
import sq
sq.traj_quantile(traj)
```

You can also do weighted quantiling if you have weights attached to each line

```py
sq.traj_quantile(traj)
```

You may want to do fancy shading, which just plots a series of quantiles as polygons with transparency. The quantils overlap, which gives
a nice blending. The outer edges of the polygons still correspond to the 95% confidence interval

```py
sq.traj_quantile(traj, fancy_shading=True)
```

Here are some further options you can modify:

```py
sq.traj_quantile(traj, fancy_shading=True, lower_q_bound=1/3, upper_q_bound=2/3, levels=100, color='red', alpha=0.01)
```

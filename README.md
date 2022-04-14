# shadyquant😎

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/whitead/shadyquant)
[![PyPI version](https://badge.fury.io/py/shadyquant.svg)](https://badge.fury.io/py/shadyquant)

This python package allows you to quantile and plot lines where you have multiple samples, typically for visualizing uncertainty.  Your data should be shaped `(N, T)`, where `N` is the number of
samples, `T` is the dimension of your lines.

## Install

```sh
pip install shadyquant
```

## Usage

Consider you have 100 lines that you want to compute confidence intervals (quantiles) on:

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2,1000)
y = np.sin(x)
plt.plot(x,y)
```
![image](https://user-images.githubusercontent.com/908389/163302232-2b719ee6-aeb3-4c37-a68c-15c69d4e57c9.png)

I'll make 100 examples of this plot, each scaled by a random number.

```py
w = np.random.normal(size=100)**2
traj = y + y * w[:, None]
plt.plot(traj.T, color='C0')
plt.show()
```
![image](https://user-images.githubusercontent.com/908389/163302143-42fdebee-afc8-4ec6-b550-f5208be32e99.png)


You can use shadyquant to plot a 95% confidence interval (default):

```py
import sq
sq.traj_quantile(traj)
```
![image](https://user-images.githubusercontent.com/908389/163302155-c78fc4c6-caf6-487f-b632-5fda3d9c3fba.png)


You can also do weighted quantiling, if you have weights attached to each line

```py
sq.traj_quantile(traj, weights=w)
```

![image](https://user-images.githubusercontent.com/908389/163302172-e3ae6143-aecd-48cb-bb7a-1259e760efeb.png)


You may want to do fancy shading, which just plots a series of quantiles as polygons with transparency. The quantiles overlap, which gives
a nice blending. The outer edges of the polygons still correspond to the 95% confidence interval.

```py
sq.traj_quantile(traj, fancy_shading=True)
```

![image](https://user-images.githubusercontent.com/908389/163302179-cec09ee7-c870-48be-abcd-5575f15c7a31.png)


Here are some further options you can modify:

```py
plt.figure(figsize=(8, 3))
ax = plt.gca()
sq.traj_quantile(
    traj,
    ax=ax,
    fancy_shading=True,
    lower_q_bound=1 / 3,
    upper_q_bound=2 / 3,
    levels=100,
    color="red",
    alpha=0.01,
)
```

![image](https://user-images.githubusercontent.com/908389/163302191-7b2a8000-d2b1-4902-ad07-4bd7afd650dc.png)

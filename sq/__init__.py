import numpy as np
import matplotlib.pyplot as plt

from .version import __version__


def weighted_quantile(values, quantiles, sample_weight=None):
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    if not (np.all(quantiles >= 0) and np.all(quantiles <= 1)):
        raise ValueError("quantiles should be in [0, 1]")

    sorter = np.argsort(values)
    values = values[sorter]
    sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)


def traj_quantile(
    trajs,
    weights=None,
    means=False,
    lower_q_bound=0.025,
    upper_q_bound=0.975,
    ax=None,
    color="C0",
    alpha=0.1,
    fancy_shading=False,
    levels=30,
):
    if lower_q_bound + upper_q_bound != 1.0:
        raise ValueError("lower and upper quantile bounds should sum up to 1.0.")
    if weights is None:
        w = np.ones(trajs.shape[0])
    else:
        w = weights
    if ax is None:
        ax = plt.gca()
    w /= np.sum(w)
    x = range(trajs.shape[1])
    fancy_lower_q_bounds = np.linspace(lower_q_bound, 0.5, levels)
    fancy_higher_q_bounds = 1 - fancy_lower_q_bounds
    for n in range(levels):
        # compute quantiles
        if not fancy_shading:
            lower_q_bound = fancy_lower_q_bounds[0]
            upper_q_bound = fancy_higher_q_bounds[0]
        else:
            lower_q_bound = fancy_lower_q_bounds[n]
            upper_q_bound = fancy_higher_q_bounds[n]
        # weighted quantiles doesn't support axis
        # fake it using apply_along
        qtrajs = np.apply_along_axis(
            lambda x: weighted_quantile(
                x, [lower_q_bound, 1 / 2, upper_q_bound], sample_weight=w
            ),
            0,
            trajs,
        )
        if means:
            # approximate quantiles as distance from median applied to mean
            mtrajs = np.sum(trajs * w[:, np.newaxis], axis=0)
            qtrajs[0] = qtrajs[0] - qtrajs[1] + mtrajs
            qtrajs[2] = qtrajs[2] - qtrajs[1] + mtrajs
            qtrajs[1] = mtrajs
        ax.fill_between(
            x,
            qtrajs[0],
            qtrajs[-1],
            alpha=alpha,
            color=color,
            linewidth=0.0,
            rasterized=True,
        )
        if n == 0:
            ax.plot(x, qtrajs[1], color=color)
            if not fancy_shading:
                ax.plot(x, qtrajs[0], color=color, alpha=0.4, linewidth=1)
                ax.plot(x, qtrajs[2], color=color, alpha=0.4, linewidth=1)
        if not fancy_shading:
            break

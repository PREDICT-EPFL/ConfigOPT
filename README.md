<div align="center">
  <img src="https://github.com/PREDICT-EPFL/ConfigOPT/website/figs/logo.png"><br><br>
</div>

# Constrained Efficient Global Optimization 
Python implementation of CONstrained efFIcient Global optimization (CONFIG) with Gaussian processes. CONFIG is a data-driven efficient global optimization toolbox. 
 By sequentially and adaptively evaluting different candidate solutions under the guidance of Gaussian process surrogates, CONFIG algorithm can efficiently identify globally optimal solution for constrained black-box optimization problems with potentially non-convex and multi-modal functions. CONFIG is particularly useful when the black-box functions are expensive to evaluate.

## Install
Under the directory where [README.md](./README.md) is, run `pip install .`. 

## Quick Start
In the directory "./scripts", we provide a notebook to demonstrate the usage of the toolbox. 

## How does it work?

ConfigOPT works by constructing a surrogate model of functions (Gaussian process) that best describes the unknown function using historical samples. As the number of samples grows, the accuracy of the surrogate model improves, and the algorithm becomes more certain of where the optimal solution is.

In each step, our method solves an auxilliary optimization problem that, despite still being a hard problem, is cheaper and grid-search or other methods can be applied. The optimal solution of this auxilliary problem represents the most valuable point to sample for finding the constrained global optimal solution. 

## Supported Algorithms
We recommend the CONFIG algorithm, which has demonstrated 
good convergence property to global optimal solution both in theory and in
practice. But to allow more flexibility for user's choice, we also implement the
following popular algorithms.
* Constrained EI.
* Primal-dual.
* EPBO.


Citation
============

If you used this package in your research, we appreciate that you can cite the
following papers:

```
@article{xu2022config,
  title={CONFIG: Constrained Efficient Global Optimization for Closed-Loop Control System Optimization with Unmodeled Constraints},
  author={Xu, Wenjie and Jiang, Yuning and Svetozarevic, Bratislav and Jones, Colin N},
  journal={arXiv preprint arXiv:2211.11822},
  year={2022}
}
@article{xu2022constrained,
  title={Constrained Efficient Global Optimization of Expensive Black-box Functions},
  author={Xu, Wenjie and Jiang, Yuning and Jones, Colin N},
  journal={arXiv preprint arXiv:2211.00162},
  year={2022}
}
```

# Dependencies
* Numpy
* SafeOPT



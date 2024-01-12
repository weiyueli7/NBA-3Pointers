# NBA Players Salaries: The Impact of 3-Point Shooting

Explore the presentation [here](https://docs.google.com/presentation/d/1P1KvWU4fqYWyi8WHpxwmTxv_ki-IVpbAMuxcHoqxYD8/edit?usp=sharing). The final paper is selected as a standout research paper from prior years and is accessible at [here](https://sites.google.com/site/ec191cullen/prior-papers?authuser=0).

## Introduction

This project examines the influence of 3-point shooting abilities on NBA players' salaries. We delve into whether excelling in 3-pointers correlates with higher salaries, considering various factors and statistical models.

## Getting Started

### Prerequisites

For a seamless experience, it's advisable to use a conda environment. You can create and activate a conda environment named `nba3` with Python 3.9 by following these commands:

```bash
conda create -n nba3 python=3.9
conda activate nba3
pip install -r requirements.txt
```

### Deployment

To execute the regression models and generate visualizations, use:

```bash
pythone main.py
```

For a detailed guide on `main.py`, including available arguments, use:

```bash
python main.py -h
```

To incorporate ESPN salary data:

```bash
python3 main.py --salary_source espn
```

Configuration adjustments can be made in the [model_configs](model_configs) files. The results from the Ordinary Least Squares (OLS) models and related figures will be stored in the [results](results) folder.


## Author

* [Weiyue Li](https://weiyueli7.github.io/)


## Acknowledgments

Special thanks to Professor [Julie Cullen](https://econweb.ucsd.edu/~jbcullen/) and Professor [Emanuel Vespa](https://sites.google.com/site/emanuelvespa/) for their invaluable guidance and support in this research.

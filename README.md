<h1 align='center'> DNA analyser IBP </h1>
<br />
<div align="center">
    <a href="https://pypi.org/project/dna-analyser-ibp/">
    <img src="https://img.shields.io/badge/Version 3.6.0-green?style=for-the-badge" alt='package_version'/>
    </a>
    <img src="https://img.shields.io/badge/Python 3.10+-00599C?style=for-the-badge&logo=python&logoColor=white" alt='python_version'/>
    <img src="https://img.shields.io/badge/jupyter-gray?style=for-the-badge&logo=jupyter" alt='jupyter'/>
    <a href="https://choosealicense.com/licenses/gpl-3.0/">
            <img src="https://img.shields.io/badge/gnu-white?style=for-the-badge&logo=gnu&logoColor=black" alt='licence'/>
    </a>
</div>
<br />

Tool for creating R-loop tracker, P53predictor, G4Killer and G4Hunter analysis. Work as API wrapper for IBP DNA analyzer API [bioinformatics.ibp](http://bioinformatics.ibp.cz/).
Currently working with an instance of DNA analyser server running on http://bioinformatics.ibp.cz computational core but can be switched 
to the local instance of the server.

# Getting Started

## Prerequisites

python >= 3.10

## Installing

To install test version from [Pypi](https://pypi.org/project/dna-analyser-ibp/).

```commandline
pipenv install dna-analyser-ibp
```

```commandline
pip install dna-analyser-ibp
```
## Quick start

DNA analyser uses `pandas.Dataframe` or `pandas.Series`. Firstly the user  has to create `Api` object and login to API.
```python
from DNA_analyser_IBP.api import Api

API = Api()
```
```python
Enter your email        example@example.cz
Enter your password     ········

2020-09-16 18:51:17.943398 [INFO]: User host is trying to login ...
2020-09-16 18:51:17.990580 [INFO]: User host is successfully loged in ...
```
If DNA analyser API server is not running on http://bioinformatics.ibp.cz then you have to set server paramether to create `Api` object.
```python
from DNA_analyser_IBP.api import Api

API = Api(
    server='http://hostname:port/api'
)
```

## Sequence uploading
Sequences can be uploaded from NCBI, plain text or text file. Example bellow illustrates NCBI sequence uploading `Homo sapiens chromosome 12`.
```python
API.sequence.ncbi_creator(
    circular= True,
    tags=['Homo','sapiens', 'chromosome'],
    name='Homo sapiens chromosome 12',
    ncbi_id='NC_000012.12'
)

API.sequence.load_all(
    tags=['Homo']
)
```

## G4Hunter
G4Hunter is a tool for prediction of G-quadruplex propensity in nucleic acids, this algorithm considers G-richness and G-skewness of a tested sequence and shows a quadruplex propensity score. 
```python
sapiens = API.g4hunter.load_all(
    tags=['Homo']
)

API.g4hunter.analyse_creator(
    sequence=sapiens,
    tags=['analyse','Homo', 'sapiens'],
    threshold=1.4,
    window_size=30
)
```
To load results of G4Hunter analysis.
```python
API.g4hunter.load_all(
    tags=['analyse', 'Homo', 'sapiens']
) 
```

## R-loop tracker
 R-loop tracker is a toll for prediction of R-loops in nucleic acids. The algorithms search for R-loop initiation zone based on presence of G-clusters and R-loop elongation zone containing at least 40% of Guanine density.
```python
sapiens = API.g4hunter.load_all(
    tags=['Homo']
)
API.rloopr.analyse_creator(
    sequence=sapiens,
    tags=['analyse', 'Homo', 'sapiens'],
    riz_2g_cluster=True,
    riz_3g_cluster=False
)
```
To load results of R-loop tracker analysis.
```python
API.rloopr.load_all(
    tags=['analyse', 'Homo', 'sapiens']
) 
```

## G4Killer
G4Killer algorithm allows to mutate DNA sequences with desired G4Hunter score with minimal mutation steps.
```python
API.g4killer.run(
    sequence='AATTATTTGGAAAGGGGGGGTTTTCCGA',
    threshold=0.5
) 

API.g4killer.run_multiple(
    sequences=[
        'AATTATTTGGAAAGGGGGGGTTTTCCGA',
        'AATTATTTGGAAAGGGGGGGTTTTCCGA'
    ],
    threshold=0.5
)
```
## P53 predictor
P53 binding predictor for 20 base pairs sequences. 
```python
API.p53.run(
    sequence='GGACATGCCCGGGCATGTCC'
)

API.p53.run_multiple(
    sequences=[
        'GGACATGCCCGGGCATGTCC',
        'GGACATGCCCGGGCATGTCC'
    ]
) 
```

# Development

## Dependencies

* requests = "2.31.0"
* pandas = "2.0.0"
* tqdm = "4.66.0"
* pyjwt = "2.8.0"
* matplotlib = "3.7.2"
* requests-toolbelt = "1.0.0"
* tenacity = "8.2.3"

## DEV dependencies

* pytest = "7.4.2"


## Tests

To run tests only when downloaded directly from this repository.

```commandline
pytest -v tests/
```

## Authors

* **Patrik Kaura** - *Main developer* - [patrikkaura](https://github.com/patrikkaura)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details.

<div align="center">
    <img src="https://gitlab.com/PatrikKaura/dna_analyser_ibp_logos/-/raw/master/logo.png" alt='logo' width='300px'>
    <br/>
    <br/>
    <a href="https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commits/master">
        <img alt="pipeline status" src="https://gitlab.com/PatrikKaura/DNA_analyser_IBP/badges/master/pipeline.svg" />
    </a>
    <a href="https://pypi.org/project/dna-analyser-ibp/">
        <img src="https://img.shields.io/badge/version-3.4.1-brightgreen.svg" alt='version'/>
    </a>
    <img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt='python_version'/>
    <img src="https://img.shields.io/badge/python-3.7-brightgreen.svg" alt='python_version'/>
    <img src="https://img.shields.io/badge/python-3.8-brightgreen.svg" alt='python_version'/>
    <a href="https://choosealicense.com/licenses/gpl-3.0/">
        <img src='https://img.shields.io/badge/licence-GNU%20v3.0-blue.svg' alt='licence'/>
    </a>
    <h1 align='center'> DNA analyser IBP </h1>
</div>


Tool for creating R-loop tracker, P53predictor, G4Killer and G4Hunter analysis. Work as API wrapper for IBP DNA analyzer API [bioinformatics.ibp](http://bioinformatics.ibp.cz/).
Currently working with an instance of DNA analyser server running on http://bioinformatics.ibp.cz computational core but can be switched 
to the local instance of the server.

# Getting Started

## Prerequisites

python >= 3.6

## Installing

To install test version from [Pypi](https://pypi.org/project/dna-analyser-ibp/).

```commandline
pipenv install dna-analyser-ibp
```

```commandline
pip install dna-analyser-ibp
```

## Documentation

Methods are documented in the following [documentation](https://patrikkaura.gitlab.io/DNA_analyser_IBP/).

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

* tenacity >= 6.1.0
* requests >= 2.20
* requests-toolbelt >= 0.9.1
* pyjwt >= 1.7.1
* pandas >= 0.23
* matplotlib >= 3.0.3
* tqdm >= 4.28

## DEV dependencies

* pytest = "^6.0.2"
* pdoc3 = "^0.9.1"
* black = "^20.0"

## Tests

To run tests only when downloaded directly from this repository.

```commandline
pytest -v tests/
```

## Authors

* **Patrik Kaura** - *Main developer* - [patrikkaura](https://gitlab.com/PatrikKaura/)
* **Jan Kolomaznik** - *Supervisor* - [jankolomaznik](https://github.com/Kolomaznik)
* **Jiří Šťastný** - *Supervisor*

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details.

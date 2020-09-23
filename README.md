<div align="center">
    <img src="https://gitlab.com/PatrikKaura/dna_analyser_ibp_logos/-/raw/master/logo.png" alt='logo' width='300px'>
    <br/>
    <br/>
    <a href="https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commits/master">
        <img alt="pipeline status" src="https://gitlab.com/PatrikKaura/DNA_analyser_IBP/badges/master/pipeline.svg" />
    </a>
    <a href="https://pypi.org/project/dna-analyser-ibp/">
        <img src="https://img.shields.io/badge/version-3.1.4-brightgreen.svg" alt='version'/>
    </a>
    <img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt='python_version'/>
    <img src="https://img.shields.io/badge/python-3.7-brightgreen.svg" alt='python_version'/>
    <img src="https://img.shields.io/badge/python-3.8-brightgreen.svg" alt='python_version'/>
    <a href="https://choosealicense.com/licenses/gpl-3.0/">
        <img src='https://img.shields.io/badge/licence-GNU%20v3.0-blue.svg' alt='licence'/>
    </a>
    <h1 align='center'> DNA analyser IBP </h1>
</div>


Tool for creating Palindrome, P53predictor, and G4Hunter analysis. Work as API wrapper for IBP DNA analyzer API [bioinformatics.ibp](http://bioinformatics.ibp.cz/).
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
If DNA analyser API server not running on http://bioinformatics.ibp.cz then use this example to create `Api` object.
```python
from DNA_analyser_IBP.api import Api

API = Api(server='http://hostname:port/api')
```
Then upload NCBI sequence for example `Homo sapiens chromosome 12` use.
```python
API.sequence.ncbi_creator(circular= True, tags=['Homo','sapiens', 'chromosome'], name='Homo sapiens chromosome 12', ncbi_id='NC_000012.12')
```
To analyse NCBI sequence use g4hunter interface.
```python
sapiens_sequence = API.sequence.load_all(tags='Homo') # get series with sapiens sequence

# run g4hunter analyses with these params
API.g4hunter.analyse_creator(sequence=sapiens_sequence, tags=['testovaci','Homo', 'sapiens'], threshold=1.4, window_size=30)
```
Last step to see results of g4hunter analysis.
```python
sapiens = API.g4hunter.load_all(tags=['Homo']) # returns dataframe
API.g4hunter.load_results(analyse=sapiens.iloc[0]) # iloc[0] to select row from dataframe
```
## P53 / G4KILLER TOOL
To run simple tools using plain text input.
```python
# implements g4killer algorithm for generating sequence with lower gscore
API.g4killer.run(sequence='AATTATTTGGAAAGGGGGGGTTTTCCGA', threshold=0.5) 

# implements calculations of p53 binding predictor for 20 base pairs sequences 
API.p53.run(sequence='GGACATGCCCGGGCATGTCC') 
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

# Version 2.0.0 (2020-02-24)

### Feature

- MultiFasta uploader [[729d20](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/tree/729d20da3e7348206000a7783b3cd414d8d8b061)]
- Sphinx documentation [[729d20](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/tree/729d20da3e7348206000a7783b3cd414d8d8b061)]
- Anotation downloader [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
- Anotation parser [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
- Anotation + G4Hunter analyse intersection [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
- G4Hunter heatmap downloader [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
 
### Fix

- G4Hunter heatmap method add aggregation parameter [default=True] [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]

### Refactoring

- Changes in all doc strings (Goolgle style) [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
- Sequence methods encapsulated into SequenceMethods object [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]
- G4Hunter methods encapsulated into G4HunterMethods object [[58a038](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/-/commit/58a03840d37a8bf492cb5282eee195f89d5d0584)]

# Version 1.5.6 (2019-11-13)

###  Chore

-  Add .gitlab-ci.yml for test pipeline [[504976b8](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/commit/750dc01d4fafb781ab7b5aa004021c07e424ab0a)]

### Features

- Add global exception handler [[f9851e17](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/commit/f9851e1758bdc153e9302241eeeba522f7adab66)]

# Version 1.5.5 (2019-11-13)

### Features
- Add nucleci re-count endpoint (PATCH) into sequence interaces [[5f28b338](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/tree/5f28b3389fbc1cd72b9d32037538216338d65742)]
```python
# re-count process
SEQUENCES = API.sequence.load_all() # load sequences
API.sequence.nucleic_count(sequence_dataframe=SEQUENCES) # re-count sequences
```
# Version 1.5.4 (2019-10-26)

###  Bugfix

-  Fixed name in batch caller - sequence.batch.length [[43977c4f](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/commit/750dc01d4fafb781ab7b5aa004021c07e424ab0a)]

# Version 1.5.3 (2019-10-20)

### Features

-  Add batch caller for faster state checking [[750dc01d](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/commit/750dc01d4fafb781ab7b5aa004021c07e424ab0a)]

# Version 1.5.2 (2019-9-28)

### Refactoring

-  Refactoring analyse + sequence tagg policy [[f4c044b4](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/commit/f4c044b4f38d688a3466b346b325ea5e458101e7)]

# Version 1.5.1 (2019-9-28)

### Refactoring

-  Major project refactoring [[21424b85](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/tree/21424b85ddc43f2baa819a208894542338839363)]

# Version 1.5.0 (2019-9-10)

### Chore

- Project move from github to gitlab repo [[4fba6eb5](https://gitlab.com/PatrikKaura/DNA_analyser_IBP/tree/4fba6eb5f10a59fc9ed2248862948a877edf42af)]
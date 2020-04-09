# DNA_analyser_IBP.callers package

## Submodules

## DNA_analyser_IBP.callers.analyse_caller module


### class DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory(\*\*kwargs)
Bases: `object`

Abstract class for others analyse factories


#### abstract create_analyse(\*\*kwargs)
Creates analyse with different calls on Api


### class DNA_analyser_IBP.callers.analyse_caller.AnalyseModel(\*\*kwargs)
Bases: `object`

Analyse class used in g4hunter + palindrome analyse


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.DataFrame


## DNA_analyser_IBP.callers.batch_caller module


### class DNA_analyser_IBP.callers.batch_caller.BatchCaller()
Bases: `object`

Batch class used in all models to check progress


#### static get_analyse_batch_status(analyse: DNA_analyser_IBP.callers.analyse_caller.AnalyseModel, user: DNA_analyser_IBP.callers.user_caller.User)
Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)


* **Parameters**

    
    * **analyse** (*AnalyseModel*) – Analyse object


    * **user** (*User*) – user for auth



* **Returns**

    FINISH|FAILED



* **Return type**

    str



#### static get_sequence_batch_status(sequence: DNA_analyser_IBP.callers.sequence_caller.SequenceModel, user: DNA_analyser_IBP.callers.user_caller.User)
Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)


* **Parameters**

    
    * **sequence** (*SequenceModel*) – Sequence object


    * **user** (*User*) – user for auth



* **Returns**

    FINISH|FAILED



* **Return type**

    str


## DNA_analyser_IBP.callers.g4hunter_caller module


### class DNA_analyser_IBP.callers.g4hunter_caller.G4HunterAnalyse(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseModel`

G4Hunter analyse object finds guanine quadruplex in DNA/RNA sequence


### class DNA_analyser_IBP.callers.g4hunter_caller.G4HunterAnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

G4Hunter factory used for generating analyse for given sequence


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, id: str, tags: Optional[List[str]], threshold: float, window_size: int)
G4hunter analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id


    * **tags** (*Optional**[**List**[**str**]**]*) – analyse tags


    * **threshold** (*float*) – threshold for g4hunter algorithm recommended 1.2


    * **window_size** (*int*) – window size for g4hunter algorithm recommended 25



* **Returns**

    G4Hunter object



* **Return type**

    G4HunterAnalyse



### class DNA_analyser_IBP.callers.g4hunter_caller.G4HunterMethods()
Bases: `object`

G4HunterMethods holds all g4hunter server methods


#### static delete(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete analyse by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    True if delete is successfull False if not



* **Return type**

    bool



#### static export_csv(user: DNA_analyser_IBP.callers.user_caller.User, id: str, aggregate: bool = True)
Export G4Hunter results as csv output


* **Parameters**

    
    * **user** (*User*) – user for atuh


    * **id** (*str*) – g4hunter analyse id


    * **aggregate** (*bool*) – True if aggregate results else False



* **Returns**

    csv file in string



* **Return type**

    str



#### static load_all(user: DNA_analyser_IBP.callers.user_caller.User, tags: List[Optional[str]])
Load all g4hunter analyses


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **tags** (*List**[**Optional**[**str**]**]*) – filter tag for loading



* **Returns**

    G4Hunter object generator



* **Return type**

    Generator[G4HunterAnalyse, None, None], Exception



#### static load_by_id(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Load one g4hunter analyse by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    G4Hunter object



* **Return type**

    G4HunterAnalyse



#### static load_heatmap(user: DNA_analyser_IBP.callers.user_caller.User, id: str, segments: int)
Download heatmap data for G4Hunter analyse


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id


    * **segments** (*int*) – number of heatmap segments



* **Returns**

    dataFrame with heatmap data



* **Return type**

    pd.DataFrame



#### static load_result(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Load G4Hunter analyse result


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    DataFrame with G4Hunter results



* **Return type**

    pd.DataFrame


## DNA_analyser_IBP.callers.g4killer_caller module


### class DNA_analyser_IBP.callers.g4killer_caller.G4KillerAnalyse(\*\*kwargs)
Bases: `object`

G4Killer analyse object destroy guanin quadruplex and lower G-score


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.DataFrame



### class DNA_analyser_IBP.callers.g4killer_caller.G4KillerAnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

G4Killer factory used to generate analyse for given sequence string


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, sequence: str, threshold: float, complementary: bool)
G4killer analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **sequence** (*str*) – origin sequence for G4Killer procedure


    * **threshold** (*float*) – target g4hunter score in interval <0;4>


    * **complementary** (*bool*) – True if use for C sequence False for G sequence



* **Returns**

    G4KillerAnalyse object



* **Return type**

    G4KillerAnalyse


## DNA_analyser_IBP.callers.p53_caller module


### class DNA_analyser_IBP.callers.p53_caller.P53Analyse(\*\*kwargs)
Bases: `object`

P53 analyse object finds p53 protein affinity in DNA|RNA sequence.


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.Dataframe



### class DNA_analyser_IBP.callers.p53_caller.P53AnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

P53 factory used for generating analyse for given sequence.


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, sequence: str)
P53 analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **sequence** (*str*) – sequence string of lenght 20



* **Returns**

    P53Analyse object



* **Return type**

    P53Analyse


## DNA_analyser_IBP.callers.sequence_caller module


### class DNA_analyser_IBP.callers.sequence_caller.FileSequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from file


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, path: str, name: str, tags: List[Optional[str]], nucleic_type: str, format: str)
File sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **path** (*str*) – absolute path to sequence file


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **nucleic_type** (*str*) – string DNA|RNA            format (str): string FASTA|PLAIN



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



### class DNA_analyser_IBP.callers.sequence_caller.NCBISequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from NCBI database


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, name: str, tags: List[Optional[str]], ncbi_id: str)
NCBI sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **ncbi_id** (*str*) – sequence id from ([https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/))



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



### class DNA_analyser_IBP.callers.sequence_caller.SequenceFactory(\*\*kwargs)
Bases: `object`

Abstract class for others sequence factories


#### abstract create_sequence(\*\*kwargs)
Creates sequence with different calls on Api


### class DNA_analyser_IBP.callers.sequence_caller.SequenceMethods()
Bases: `object`

SequenceMethods holds all sequence server methods


#### static delete(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete sequence by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    True if delete is successfull False if not



* **Return type**

    bool



#### static load_all(user: DNA_analyser_IBP.callers.user_caller.User, tags: List[Optional[str]])
Load all sequences


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for filtering all sequences



* **Returns**

    Sequence object generator



* **Return type**

    Generator[SequenceModel, None, None]



#### static load_by_id(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete sequence by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



#### static load_data(user: DNA_analyser_IBP.callers.user_caller.User, id: str, length: int, possiotion: int, sequence_length: int)
Return string with part of sequence


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id


    * **length** (*int*) – data string length


    * **possiotion** (*int*) – data start position


    * **sequence_length** (*int*) – sequence length for check



* **Returns**

    String with part of sequence data



* **Return type**

    str



#### static nucleic_count(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Run nucleic count of sequence by given id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    True if re-count is successfull False if not



* **Return type**

    bool



### class DNA_analyser_IBP.callers.sequence_caller.SequenceModel(\*\*kwargs)
Bases: `object`

Sequence class


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.DataFrame



#### set_gc_count(nucleic_dict: dict)
Set GC count from nucleic count dict


* **Parameters**

    **nucleic_dict** (*dict*) – structure with Guanine and Cytosine counts



### class DNA_analyser_IBP.callers.sequence_caller.TextSequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from raw text or text file


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, data: str, name: str, tags: List[Optional[str]], nucleic_type: str)
Text sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **data** (*str*) – string data with sequence


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **nucleic_type** (*str*) – string DNA|RNA



* **Returns**

    Sequence object



* **Return type**

    SequenceModel


## DNA_analyser_IBP.callers.user_caller module


### class DNA_analyser_IBP.callers.user_caller.User(email: str, password: str, server: str)
Bases: `object`

User class providing information for current user

## Module contents


### class DNA_analyser_IBP.callers.User(email: str, password: str, server: str)
Bases: `object`

User class providing information for current user


### class DNA_analyser_IBP.callers.G4HunterAnalyse(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseModel`

G4Hunter analyse object finds guanine quadruplex in DNA/RNA sequence


### class DNA_analyser_IBP.callers.G4HunterAnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

G4Hunter factory used for generating analyse for given sequence


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, id: str, tags: Optional[List[str]], threshold: float, window_size: int)
G4hunter analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id


    * **tags** (*Optional**[**List**[**str**]**]*) – analyse tags


    * **threshold** (*float*) – threshold for g4hunter algorithm recommended 1.2


    * **window_size** (*int*) – window size for g4hunter algorithm recommended 25



* **Returns**

    G4Hunter object



* **Return type**

    G4HunterAnalyse



### class DNA_analyser_IBP.callers.G4HunterMethods()
Bases: `object`

G4HunterMethods holds all g4hunter server methods


#### static delete(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete analyse by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    True if delete is successfull False if not



* **Return type**

    bool



#### static export_csv(user: DNA_analyser_IBP.callers.user_caller.User, id: str, aggregate: bool = True)
Export G4Hunter results as csv output


* **Parameters**

    
    * **user** (*User*) – user for atuh


    * **id** (*str*) – g4hunter analyse id


    * **aggregate** (*bool*) – True if aggregate results else False



* **Returns**

    csv file in string



* **Return type**

    str



#### static load_all(user: DNA_analyser_IBP.callers.user_caller.User, tags: List[Optional[str]])
Load all g4hunter analyses


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **tags** (*List**[**Optional**[**str**]**]*) – filter tag for loading



* **Returns**

    G4Hunter object generator



* **Return type**

    Generator[G4HunterAnalyse, None, None], Exception



#### static load_by_id(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Load one g4hunter analyse by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    G4Hunter object



* **Return type**

    G4HunterAnalyse



#### static load_heatmap(user: DNA_analyser_IBP.callers.user_caller.User, id: str, segments: int)
Download heatmap data for G4Hunter analyse


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id


    * **segments** (*int*) – number of heatmap segments



* **Returns**

    dataFrame with heatmap data



* **Return type**

    pd.DataFrame



#### static load_result(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Load G4Hunter analyse result


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – g4hunter analyse id



* **Returns**

    DataFrame with G4Hunter results



* **Return type**

    pd.DataFrame



### class DNA_analyser_IBP.callers.G4KillerAnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

G4Killer factory used to generate analyse for given sequence string


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, sequence: str, threshold: float, complementary: bool)
G4killer analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **sequence** (*str*) – origin sequence for G4Killer procedure


    * **threshold** (*float*) – target g4hunter score in interval <0;4>


    * **complementary** (*bool*) – True if use for C sequence False for G sequence



* **Returns**

    G4KillerAnalyse object



* **Return type**

    G4KillerAnalyse



### class DNA_analyser_IBP.callers.G4KillerAnalyse(\*\*kwargs)
Bases: `object`

G4Killer analyse object destroy guanin quadruplex and lower G-score


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.DataFrame



### class DNA_analyser_IBP.callers.P53Analyse(\*\*kwargs)
Bases: `object`

P53 analyse object finds p53 protein affinity in DNA|RNA sequence.


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.Dataframe



### class DNA_analyser_IBP.callers.P53AnalyseFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.analyse_caller.AnalyseFactory`

P53 factory used for generating analyse for given sequence.


#### create_analyse(user: DNA_analyser_IBP.callers.user_caller.User, sequence: str)
P53 analyse factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **sequence** (*str*) – sequence string of lenght 20



* **Returns**

    P53Analyse object



* **Return type**

    P53Analyse



### class DNA_analyser_IBP.callers.FileSequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from file


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, path: str, name: str, tags: List[Optional[str]], nucleic_type: str, format: str)
File sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **path** (*str*) – absolute path to sequence file


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **nucleic_type** (*str*) – string DNA|RNA            format (str): string FASTA|PLAIN



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



### class DNA_analyser_IBP.callers.NCBISequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from NCBI database


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, name: str, tags: List[Optional[str]], ncbi_id: str)
NCBI sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **ncbi_id** (*str*) – sequence id from ([https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/))



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



### class DNA_analyser_IBP.callers.TextSequenceFactory(\*\*kwargs)
Bases: `DNA_analyser_IBP.callers.sequence_caller.SequenceFactory`

Sequence factory used for generating sequence from raw text or text file


#### create_sequence(user: DNA_analyser_IBP.callers.user_caller.User, circular: bool, data: str, name: str, tags: List[Optional[str]], nucleic_type: str)
Text sequence factory


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **circular** (*bool*) – True if sequence is circular False if not


    * **data** (*str*) – string data with sequence


    * **name** (*str*) – sequence name


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for sequence filtering


    * **nucleic_type** (*str*) – string DNA|RNA



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



### class DNA_analyser_IBP.callers.SequenceModel(\*\*kwargs)
Bases: `object`

Sequence class


#### get_dataframe()
Return pandas dataframe for current object


* **Returns**

    dataframe with object data



* **Return type**

    pd.DataFrame



#### set_gc_count(nucleic_dict: dict)
Set GC count from nucleic count dict


* **Parameters**

    **nucleic_dict** (*dict*) – structure with Guanine and Cytosine counts



### class DNA_analyser_IBP.callers.SequenceMethods()
Bases: `object`

SequenceMethods holds all sequence server methods


#### static delete(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete sequence by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    True if delete is successfull False if not



* **Return type**

    bool



#### static load_all(user: DNA_analyser_IBP.callers.user_caller.User, tags: List[Optional[str]])
Load all sequences


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **tags** (*List**[**Optional**[**str**]**]*) – tags for filtering all sequences



* **Returns**

    Sequence object generator



* **Return type**

    Generator[SequenceModel, None, None]



#### static load_by_id(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Delete sequence by id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    Sequence object



* **Return type**

    SequenceModel



#### static load_data(user: DNA_analyser_IBP.callers.user_caller.User, id: str, length: int, possiotion: int, sequence_length: int)
Return string with part of sequence


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id


    * **length** (*int*) – data string length


    * **possiotion** (*int*) – data start position


    * **sequence_length** (*int*) – sequence length for check



* **Returns**

    String with part of sequence data



* **Return type**

    str



#### static nucleic_count(user: DNA_analyser_IBP.callers.user_caller.User, id: str)
Run nucleic count of sequence by given id


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **id** (*str*) – sequence id



* **Returns**

    True if re-count is successfull False if not



* **Return type**

    bool



### class DNA_analyser_IBP.callers.BatchCaller()
Bases: `object`

Batch class used in all models to check progress


#### static get_analyse_batch_status(analyse: DNA_analyser_IBP.callers.analyse_caller.AnalyseModel, user: DNA_analyser_IBP.callers.user_caller.User)
Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)


* **Parameters**

    
    * **analyse** (*AnalyseModel*) – Analyse object


    * **user** (*User*) – user for auth



* **Returns**

    FINISH|FAILED



* **Return type**

    str



#### static get_sequence_batch_status(sequence: DNA_analyser_IBP.callers.sequence_caller.SequenceModel, user: DNA_analyser_IBP.callers.user_caller.User)
Return sequence batch status (CREATED, WAITING, RUNNING, FINISH, FAILED)


* **Parameters**

    
    * **sequence** (*SequenceModel*) – Sequence object


    * **user** (*User*) – user for auth



* **Returns**

    FINISH|FAILED



* **Return type**

    str

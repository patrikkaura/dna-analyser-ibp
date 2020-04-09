# DNA_analyser_IBP.interfaces package

## Submodules

## DNA_analyser_IBP.interfaces.analyse_interface module


### class DNA_analyser_IBP.interfaces.analyse_interface.AnalyseInterface()
Bases: `object`

Interface for api endpoint caller has to have at least this methods


#### abstract analyse_creator(\*args)

#### abstract delete(obj: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])

#### abstract load_all(filter_tag: Optional[List[str]])

#### abstract load_by_id(id: str)
## DNA_analyser_IBP.interfaces.extras_interface module


### exception DNA_analyser_IBP.interfaces.extras_interface.DownloadException()
Bases: `Exception`


### class DNA_analyser_IBP.interfaces.extras_interface.Extras()
Bases: `object`


#### annotation_analyse_pair_creator(\*, analyse_list: List[str], annotation_list: List[str])
Make list of file pairs for annotation analysis


* **Parameters**

    
    * **analyse_list** (*List**[**str**]*) – list of analyse files made by glog


    * **annotation_list** (*List**[**str**]*) – list of annotation files made by glob



* **Returns**

    file pairs based on their similar names



* **Return type**

    List[str]



#### annotation_downloader(path: str, filename: str, ncbi_id: str)
Annotation downloader used to download annotation by NCBI ID


* **Parameters**

    
    * **path** (*str*) – path where to store new annotation file


    * **filename** (*str*) – filename of new annotation file


    * **ncbi_id** (*str*) – ncbi id used for identication of annotation on remote server



#### annotation_overlay(\*, analyse_file: str, annotation_file: str, area_size: int = 100, overlay_path: str = '')
Create overlay dataframe for given G4Hunter analyse and parsed annotation file


* **Parameters**

    
    * **analyse_file** (*str*) – path to g4hunter analyse result file


    * **annotation_file** (*str*) – path to parsed annotation file


    * **area_size** (*int*) – size of overlay region outside annotation [Default=100]


    * **overlay_path** (*str*) – overlay csv file path (if want to save to csv) [Default=””]



* **Returns**

    intersection result



* **Return type**

    (pd.DataFrame)



#### annotation_parser(annotation_path: str, parsed_path: str)
Parse annotation file into [DataFrame]


* **Parameters**

    
    * **annotation_path** (*str*) – annotation file system path


    * **parsed_path** (*str*) – parsed annotation file in CSV



#### multifasta_to_fasta(\*, path: str, out_path: str)
Split one MultiFASTA file into multiple FASTA files


* **Parameters**

    
    * **path** (*str*) – absolute system path into folder with MultiFASTA


    * **out_path** (*str*) – absolute system path into output folder with FASTAs


## DNA_analyser_IBP.interfaces.g4hunter_interface module


### class DNA_analyser_IBP.interfaces.g4hunter_interface.G4Hunter(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.analyse_interface.AnalyseInterface`

Api interface for g4hunter analyse caller


#### analyse_creator(tags: Optional[List[str]] = None, \*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series], threshold: float, window_size: int)
Create G4hunter analyse


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for analyse filtering [default=None]


    * **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – one or many sequences to analyse


    * **threshold** (*float*) – g4hunter threshold recommended 1.2


    * **window_size** (*int*) – g4hunter window size recommended 25



#### delete(\*, analyse: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Delete G4Hunter analyse


* **Parameters**

    **analyse** (*Union**[**pd.DataFrame**, **pd.Series**]*) – g4hunter analyse [Dataframe|Series]



#### export_csv(\*, analyse: Union[pandas.core.frame.DataFrame, pandas.core.series.Series], path: str, aggregate: bool = True)
Export G4Hunter analyses result into csv files


* **Parameters**

    
    * **analyse** (*Union**[**pd.DataFrame**, **pd.Series**]*) – g4hunter analyse Dataframe|Series


    * **path** (*str*) – absolute system path to output folder


    * **aggregate** (*bool*) – True = aggregation, False = no aggregation



#### get_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: pandas.core.series.Series)
Return dataframe with heatmap data


* **Parameters**

    
    * **segments** (*Optional**[**int**]*) – g4hunter analyse series [Default=31]


    * **coverage** (*Optional**[**bool**]*) – True = coverage heatmap False = count heatmap [default=False]


    * **analyse** (*pd.Series*) – analyse series data to get heatmap



* **Returns**

    raw data used to create heatmap



* **Return type**

    pd.DataFrame



#### load_all(tags: Optional[List[str]] = None)
Return all or filtered g4hunter analyses in dataframe


* **Parameters**

    **tags** (*Optional**[**List**[**str**]**]*) – tags for analyse filtering [default=None]



* **Returns**

    Dataframe with g4hunter analyses



* **Return type**

    pd.DataFrame



#### load_by_id(\*, id: str)
Return g4hunter analyse in dataframe


* **Parameters**

    **id** (*str*) – g4hunter analyse id



* **Returns**

    Dataframe with g4hunter analyse



* **Return type**

    pd.DataFrame



#### load_results(\*, analyse: pandas.core.series.Series)
Return g4hunter analyses results in dataframe


* **Parameters**

    **analyse** (*pd.Series*) – g4hunter analyse series



* **Returns**

    Dataframe with g4hunter results



* **Return type**

    pd.DataFrame



#### save_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], path: str)
Save seaborn graph with heatmap
:param segments: g4hunter analyse series [Default=31]
:type segments: Optional[int]
:param coverage: True = coverage heatmap False = count heatmap [default=False]
:type coverage: Optional[bool]
:param analyse: analyse series or analyses dataframe to get heatmap
:type analyse: Union[pd.Series, pd.DataFrame]
:param path: outputh path where to save heatmap SVGs
:type path: str


#### show_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: pandas.core.series.Series)
Return seaborn graph with heatmap


* **Parameters**

    
    * **segments** (*Optional**[**int**]*) – g4hunter analyse series [Default=31]


    * **coverage** (*Optional**[**bool**]*) – True = coverage heatmap False = count heatmap [default=False]


    * **analyse** (*pd.Series*) – analyse series data to get heatmap



* **Returns**

    seaborn graph with g4hunter heatmap



* **Return type**

    pyplot


## DNA_analyser_IBP.interfaces.g4killer_interface module


### class DNA_analyser_IBP.interfaces.g4killer_interface.G4Killer(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.tool_interface.ToolInterface`

Api interface for g4killer analyse caller


#### run(complementary: bool = False, \*, sequence: str, threshold: float)
Run G4killer tool


* **Parameters**

    
    * **complementary** (*bool*) – True if use for C sequence False for G sequence [default=False]


    * **sequence** (*str*) – original sequence


    * **threshold** (*float*) – G4hunter target score in interval (0;4)



* **Returns**

    Dataframe with G4killer result



* **Return type**

    pd.DataFrame


## DNA_analyser_IBP.interfaces.p53_interface module


### class DNA_analyser_IBP.interfaces.p53_interface.P53(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.tool_interface.ToolInterface`

Api interface for p53 caller


#### run(\*, sequence: str)
Run P53 tool


* **Parameters**

    **sequence** (*str*) – sequence [length=20] to analyse



* **Returns**

    Dataframe with P53predictor result



* **Return type**

    pd.DataFrame


## DNA_analyser_IBP.interfaces.sequence_interface module


### class DNA_analyser_IBP.interfaces.sequence_interface.Sequence(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `object`


#### delete(\*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Delete sequence by given dataframe|series


* **Parameters**

    **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – sequence or multiple sequences



#### file_creator(tags: Optional[List[str]] = None, circular: bool = True, nucleic_type: str = 'DNA', \*, path: str, name: str, format: str)
Create sequence from [TEXT|FASTA] file


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **name** (*str*) – sequence name


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **format** (*str*) – string FASTA|PLAIN


    * **path** (*str*) – absolute path to [TEXT|FASTA] file



#### load_all(tags: Optional[List[str]] = None)
Return all or filtered sequences in dataframe


* **Parameters**

    **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]



* **Returns**

    Dataframe with sequences



* **Return type**

    pd.DataFrame



#### load_by_id(\*, id: str)
Return sequence in dataframe


* **Parameters**

    **id** (*str*) – sequence id



* **Returns**

    Dataframe with sequence



* **Return type**

    pd.DataFrame



#### load_data(length: Optional[int] = 100, possition: Optional[int] = 0, \*, sequence: pandas.core.series.Series)
Return slice of sequence data in string


* **Parameters**

    
    * **length** (*Optional**[**int**]*) – sequence data length in interval <0;1000> [default=100]


    * **possition** (*Optional**[**int**]*) – data start position [default=0]


    * **sequence** (*pd.Series*) – sequence in pd.Series



* **Returns**

    sequence data



* **Return type**

    str



#### multifasta_creator(tags: Optional[List[str]] = None, circular: bool = False, \*, path: str, nucleic_type: str)
Create sequence from [MultiFASTA] file


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **path** (*str*) – absolute path to [TEXT|FASTA] file



#### ncbi_creator(tags: Optional[List[str]] = None, circular: bool = True, \*, name: str, ncbi_id: str)
Create sequence from NCBI


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **name** (*str*) – sequence name


    * **ncbi_id** (*str*) – sequence id from [https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/)



#### nucleic_count(\*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Re-count nucleotides for given sequence dataframe|series


* **Parameters**

    **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – sequence or multiple sequences



#### text_creator(circular: bool = True, tags: Optional[List[str]] = None, nucleic_type: str = 'DNA', \*, string: str, name: str)
Create sequence from string


* **Parameters**

    
    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **string** (*str*) – sequence string


    * **name** (*str*) – sequence name


## DNA_analyser_IBP.interfaces.tool_interface module


### class DNA_analyser_IBP.interfaces.tool_interface.ToolInterface()
Bases: `object`

Interface for api endpoint caller has to have at least this methods


#### abstract run(\*args)
## Module contents


### class DNA_analyser_IBP.interfaces.G4Hunter(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.analyse_interface.AnalyseInterface`

Api interface for g4hunter analyse caller


#### analyse_creator(tags: Optional[List[str]] = None, \*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series], threshold: float, window_size: int)
Create G4hunter analyse


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for analyse filtering [default=None]


    * **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – one or many sequences to analyse


    * **threshold** (*float*) – g4hunter threshold recommended 1.2


    * **window_size** (*int*) – g4hunter window size recommended 25



#### delete(\*, analyse: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Delete G4Hunter analyse


* **Parameters**

    **analyse** (*Union**[**pd.DataFrame**, **pd.Series**]*) – g4hunter analyse [Dataframe|Series]



#### export_csv(\*, analyse: Union[pandas.core.frame.DataFrame, pandas.core.series.Series], path: str, aggregate: bool = True)
Export G4Hunter analyses result into csv files


* **Parameters**

    
    * **analyse** (*Union**[**pd.DataFrame**, **pd.Series**]*) – g4hunter analyse Dataframe|Series


    * **path** (*str*) – absolute system path to output folder


    * **aggregate** (*bool*) – True = aggregation, False = no aggregation



#### get_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: pandas.core.series.Series)
Return dataframe with heatmap data


* **Parameters**

    
    * **segments** (*Optional**[**int**]*) – g4hunter analyse series [Default=31]


    * **coverage** (*Optional**[**bool**]*) – True = coverage heatmap False = count heatmap [default=False]


    * **analyse** (*pd.Series*) – analyse series data to get heatmap



* **Returns**

    raw data used to create heatmap



* **Return type**

    pd.DataFrame



#### load_all(tags: Optional[List[str]] = None)
Return all or filtered g4hunter analyses in dataframe


* **Parameters**

    **tags** (*Optional**[**List**[**str**]**]*) – tags for analyse filtering [default=None]



* **Returns**

    Dataframe with g4hunter analyses



* **Return type**

    pd.DataFrame



#### load_by_id(\*, id: str)
Return g4hunter analyse in dataframe


* **Parameters**

    **id** (*str*) – g4hunter analyse id



* **Returns**

    Dataframe with g4hunter analyse



* **Return type**

    pd.DataFrame



#### load_results(\*, analyse: pandas.core.series.Series)
Return g4hunter analyses results in dataframe


* **Parameters**

    **analyse** (*pd.Series*) – g4hunter analyse series



* **Returns**

    Dataframe with g4hunter results



* **Return type**

    pd.DataFrame



#### save_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: Union[pandas.core.series.Series, pandas.core.frame.DataFrame], path: str)
Save seaborn graph with heatmap
:param segments: g4hunter analyse series [Default=31]
:type segments: Optional[int]
:param coverage: True = coverage heatmap False = count heatmap [default=False]
:type coverage: Optional[bool]
:param analyse: analyse series or analyses dataframe to get heatmap
:type analyse: Union[pd.Series, pd.DataFrame]
:param path: outputh path where to save heatmap SVGs
:type path: str


#### show_heatmap(segments: Optional[int] = 31, coverage: Optional[bool] = False, \*, analyse: pandas.core.series.Series)
Return seaborn graph with heatmap


* **Parameters**

    
    * **segments** (*Optional**[**int**]*) – g4hunter analyse series [Default=31]


    * **coverage** (*Optional**[**bool**]*) – True = coverage heatmap False = count heatmap [default=False]


    * **analyse** (*pd.Series*) – analyse series data to get heatmap



* **Returns**

    seaborn graph with g4hunter heatmap



* **Return type**

    pyplot



### class DNA_analyser_IBP.interfaces.G4Killer(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.tool_interface.ToolInterface`

Api interface for g4killer analyse caller


#### run(complementary: bool = False, \*, sequence: str, threshold: float)
Run G4killer tool


* **Parameters**

    
    * **complementary** (*bool*) – True if use for C sequence False for G sequence [default=False]


    * **sequence** (*str*) – original sequence


    * **threshold** (*float*) – G4hunter target score in interval (0;4)



* **Returns**

    Dataframe with G4killer result



* **Return type**

    pd.DataFrame



### class DNA_analyser_IBP.interfaces.P53(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `DNA_analyser_IBP.interfaces.tool_interface.ToolInterface`

Api interface for p53 caller


#### run(\*, sequence: str)
Run P53 tool


* **Parameters**

    **sequence** (*str*) – sequence [length=20] to analyse



* **Returns**

    Dataframe with P53predictor result



* **Return type**

    pd.DataFrame



### class DNA_analyser_IBP.interfaces.Sequence(user: DNA_analyser_IBP.callers.user_caller.User)
Bases: `object`


#### delete(\*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Delete sequence by given dataframe|series


* **Parameters**

    **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – sequence or multiple sequences



#### file_creator(tags: Optional[List[str]] = None, circular: bool = True, nucleic_type: str = 'DNA', \*, path: str, name: str, format: str)
Create sequence from [TEXT|FASTA] file


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **name** (*str*) – sequence name


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **format** (*str*) – string FASTA|PLAIN


    * **path** (*str*) – absolute path to [TEXT|FASTA] file



#### load_all(tags: Optional[List[str]] = None)
Return all or filtered sequences in dataframe


* **Parameters**

    **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]



* **Returns**

    Dataframe with sequences



* **Return type**

    pd.DataFrame



#### load_by_id(\*, id: str)
Return sequence in dataframe


* **Parameters**

    **id** (*str*) – sequence id



* **Returns**

    Dataframe with sequence



* **Return type**

    pd.DataFrame



#### load_data(length: Optional[int] = 100, possition: Optional[int] = 0, \*, sequence: pandas.core.series.Series)
Return slice of sequence data in string


* **Parameters**

    
    * **length** (*Optional**[**int**]*) – sequence data length in interval <0;1000> [default=100]


    * **possition** (*Optional**[**int**]*) – data start position [default=0]


    * **sequence** (*pd.Series*) – sequence in pd.Series



* **Returns**

    sequence data



* **Return type**

    str



#### multifasta_creator(tags: Optional[List[str]] = None, circular: bool = False, \*, path: str, nucleic_type: str)
Create sequence from [MultiFASTA] file


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **path** (*str*) – absolute path to [TEXT|FASTA] file



#### ncbi_creator(tags: Optional[List[str]] = None, circular: bool = True, \*, name: str, ncbi_id: str)
Create sequence from NCBI


* **Parameters**

    
    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **name** (*str*) – sequence name


    * **ncbi_id** (*str*) – sequence id from [https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/)



#### nucleic_count(\*, sequence: Union[pandas.core.frame.DataFrame, pandas.core.series.Series])
Re-count nucleotides for given sequence dataframe|series


* **Parameters**

    **sequence** (*Union**[**pd.DataFrame**, **pd.Series**]*) – sequence or multiple sequences



#### text_creator(circular: bool = True, tags: Optional[List[str]] = None, nucleic_type: str = 'DNA', \*, string: str, name: str)
Create sequence from string


* **Parameters**

    
    * **circular** (*bool*) – True if sequence is circular False if not [default=True]


    * **tags** (*Optional**[**List**[**str**]**]*) – tags for sequence filtering [default=None]


    * **nucleic_type** (*str*) – string DNA|RNA [default=DNA]


    * **string** (*str*) – sequence string


    * **name** (*str*) – sequence name



### class DNA_analyser_IBP.interfaces.Extras()
Bases: `object`


#### annotation_analyse_pair_creator(\*, analyse_list: List[str], annotation_list: List[str])
Make list of file pairs for annotation analysis


* **Parameters**

    
    * **analyse_list** (*List**[**str**]*) – list of analyse files made by glog


    * **annotation_list** (*List**[**str**]*) – list of annotation files made by glob



* **Returns**

    file pairs based on their similar names



* **Return type**

    List[str]



#### annotation_downloader(path: str, filename: str, ncbi_id: str)
Annotation downloader used to download annotation by NCBI ID


* **Parameters**

    
    * **path** (*str*) – path where to store new annotation file


    * **filename** (*str*) – filename of new annotation file


    * **ncbi_id** (*str*) – ncbi id used for identication of annotation on remote server



#### annotation_overlay(\*, analyse_file: str, annotation_file: str, area_size: int = 100, overlay_path: str = '')
Create overlay dataframe for given G4Hunter analyse and parsed annotation file


* **Parameters**

    
    * **analyse_file** (*str*) – path to g4hunter analyse result file


    * **annotation_file** (*str*) – path to parsed annotation file


    * **area_size** (*int*) – size of overlay region outside annotation [Default=100]


    * **overlay_path** (*str*) – overlay csv file path (if want to save to csv) [Default=””]



* **Returns**

    intersection result



* **Return type**

    (pd.DataFrame)



#### annotation_parser(annotation_path: str, parsed_path: str)
Parse annotation file into [DataFrame]


* **Parameters**

    
    * **annotation_path** (*str*) – annotation file system path


    * **parsed_path** (*str*) – parsed annotation file in CSV



#### multifasta_to_fasta(\*, path: str, out_path: str)
Split one MultiFASTA file into multiple FASTA files


* **Parameters**

    
    * **path** (*str*) – absolute system path into folder with MultiFASTA


    * **out_path** (*str*) – absolute system path into output folder with FASTAs

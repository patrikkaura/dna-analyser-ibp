# DNA_analyser_IBP package

## Subpackages


* DNA_analyser_IBP.callers package


    * Submodules


    * DNA_analyser_IBP.callers.analyse_caller module


    * DNA_analyser_IBP.callers.batch_caller module


    * DNA_analyser_IBP.callers.g4hunter_caller module


    * DNA_analyser_IBP.callers.g4killer_caller module


    * DNA_analyser_IBP.callers.p53_caller module


    * DNA_analyser_IBP.callers.sequence_caller module


    * DNA_analyser_IBP.callers.user_caller module


    * Module contents


* DNA_analyser_IBP.interfaces package


    * Submodules


    * DNA_analyser_IBP.interfaces.analyse_interface module


    * DNA_analyser_IBP.interfaces.extras_interface module


    * DNA_analyser_IBP.interfaces.g4hunter_interface module


    * DNA_analyser_IBP.interfaces.g4killer_interface module


    * DNA_analyser_IBP.interfaces.p53_interface module


    * DNA_analyser_IBP.interfaces.sequence_interface module


    * DNA_analyser_IBP.interfaces.tool_interface module


    * Module contents


## Submodules

## DNA_analyser_IBP.api module

Module with API object for manipulation with BPI REST API.


### class DNA_analyser_IBP.api.Api(\*, server: str = 'http://bioinformatics.ibp.cz:8888/api')
Bases: `object`

Api class contains all methods for working with BPI REST API.

## DNA_analyser_IBP.singleton module


### class DNA_analyser_IBP.singleton.Singleton(name, bases, attrs, \*\*kwargs)
Bases: `type`

Singleton metaclass

## DNA_analyser_IBP.statusbar module


### DNA_analyser_IBP.statusbar.status_bar(user: DNA_analyser_IBP.callers.user_caller.User, func: Callable, name: str, cls_switch: bool)
TQDM status bar


* **Parameters**

    
    * **user** (*User*) – user for auth


    * **func** (*Callable*) – function decorated by statusbar


    * **name** (*str*) – name field


    * **cls_switch** (*bool*) – True = SequenceModel, False = AnalyseModel


## DNA_analyser_IBP.utils module


### class DNA_analyser_IBP.utils.Logger()
Bases: `object`

Simple unified logger


#### static error(message: str)
Unified log messagge format [ERROR]


* **Parameters**

    **message** (*str*) – message to log



#### static info(message: str)
Unified log messagge format [INFO]


* **Parameters**

    **message** (*str*) – message to log



### DNA_analyser_IBP.utils.exception_handler(fn)
Handle exception


### DNA_analyser_IBP.utils.generate_dataframe(response: Union[dict, list])
Generate dataframe from given dict/list


* **Parameters**

    **response** (*Union**[**dict**,**list**]*) – response dict|list



* **Returns**

    dataframe with response data



* **Return type**

    pd.DataFrame



### DNA_analyser_IBP.utils.normalize_name(name: str)
Normaliza name e.g. filename|analyze name


* **Parameters**

    **name** (*str*) – string to normalize



* **Returns**

    normalized string



* **Return type**

    str



### DNA_analyser_IBP.utils.validate_email(email: str)
Validate email address


* **Parameters**

    **email** (*str*) – test string



* **Returns**

    True is string is valid email else False



* **Return type**

    bool



### DNA_analyser_IBP.utils.validate_key_response(response: requests.models.Response, status_code: int, payload_key: Optional[str] = None)
Validate and convert JSON response to dictionary


* **Parameters**

    
    * **response** (*Response*) – HTTP response


    * **status_code** (*int*) – HTTP status code


    * **payload_key** (*Optional**[**str**]*) – payload key for validation



* **Returns**

    dictionary from response payload json



* **Return type**

    dict



### DNA_analyser_IBP.utils.validate_text_response(response: requests.models.Response, status_code: int)
Validate and convert Text response to dictionary


* **Parameters**

    
    * **response** (*Response*) – HTTP response


    * **status_code** (*int*) – HTTP status code



* **Returns**

    string with response data



* **Return type**

    str


## Module contents


### class DNA_analyser_IBP.Api(\*, server: str = 'http://bioinformatics.ibp.cz:8888/api')
Bases: `object`

Api class contains all methods for working with BPI REST API.

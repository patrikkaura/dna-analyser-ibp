# config.py

from tenacity import stop_after_attempt, wait_exponential


class ServerConfig:
    """
    Server URIs
    """

    LOCALHOST: str = "http://localhost:80"
    PRODUCTION: str = "https://bioinformatics.ibp.cz:443"
    DEVELOPMENT: str = "https://bioinformatika.pef.mendelu.cz:80"


class EndpointConfig:
    """
    Server endpoints
    """

    JWT: str = "jwt"
    SEQUENCE: str = "sequence"
    G4HUNTER: str = "analyse/g4hunter"
    G4KILLER: str = "analyse/g4killer"
    P53: str = "analyse/p53predictor/tool"
    RLOOPR: str = "analyse/rloopr"


class BatchConfig:
    """
    Batch endpoints
    """

    G4HUNTER: str = "batch/cz.mendelu.dnaAnalyser.analyse.g4hunter.G4Hunter"
    SEQUENCE: str = "batch/cz.mendelu.dnaAnalyser.sequence.Sequence"
    RLOOPR: str = "batch/cz.mendelu.dnaAnalyser.analyse.rloopr.Rloop"


class ExtrasConfig:
    """
    Extras URIs
    """

    ANNOTATION: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&retmode=text&rettype=ft&id="


class TenacityConfig:
    """
    Tenacity config
    """

    WAIT = wait_exponential(multiplier=1, min=4, max=10)
    STOP = stop_after_attempt(5)


class Config:
    """
    Connector urls
    """

    SERVER_CONFIG: ServerConfig = ServerConfig()
    ENDPOINT_CONFIG: EndpointConfig = EndpointConfig()
    EXTRAS_CONFIG: ExtrasConfig = ExtrasConfig()
    BATCH_CONFIG: BatchConfig = BatchConfig()
    TENACITY_CONFIG: TenacityConfig = TenacityConfig()

from dataclasses import dataclass

@dataclass(frozen=True)
class AppCredentials():
    api_key : str
    db_user : str
    db_pass : str
    db_host : str = '127.0.0.1,1401'
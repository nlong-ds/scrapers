from typing import Any, Dict
import yaml

def read_config(config_file: str = 'config.yml') -> Dict[str, Any]:
    """
    Read config file and return a dictionary with its contents.
    """
    config = yaml.load(open(config_file, 'r'), Loader=yaml.FullLoader)
    return config
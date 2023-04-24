import os, yaml


class Config(object):
    """A Wrapper Class to get access to configs from file and from environment
    """

    def __init__(self, configfile:str = "cfg/config.yml"):
        """Constructor for Config Object

        Args:
            configfile (str, optional): Path to config file. Defaults to "cfg/config.yml".
        """
        self._config = None
        with open(configfile, 'r') as stream:
            self._config = yaml.safe_load(stream)


    def get(self, param:str, env:str="CFG", default:str=None):
        """Get parameter from environment, environment is either "CFG" (default) 
        for a parameter from the config file or "ENV" for an environment variable.

        Args:
            param (str): the parameter that is queried. Yaml subkeys can be reached
                with a.b, the dictionary is automatically parsed
            env (str, optional): The environment we are querying for, that can 
                be a block from the config file "CFG" or the "ENV". Defaults to 
                config file "CFG".
            default (str, optional): The default that is returned when the parameter 
                is not found. Defaults to "None"

        Returns:
            dict, list, str, None: The parameter content. Type conversion has to be done 
                on user side. None if the parameter was not found
        """
        if env.upper() == "ENV":
            # query environment variables
            return os.environ.get(param, default)
        elif env.upper() == "CFG":
            d = self._config
            # parse the config parameter and try to navigate the yaml
            for item in param.split("."):
                d = d.get(item, default)
            return d


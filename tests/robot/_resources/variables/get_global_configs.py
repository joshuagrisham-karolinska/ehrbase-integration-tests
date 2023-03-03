import argparse
import configparser
import os

# Environment Variable action for argparse so we can fetch the same value from env instead

class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, 
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

# Setup default config file if none is passed with --config

this_file_path = os.path.dirname(os.path.abspath(__file__))
default_config_file = os.path.join(this_file_path, 'default.ini')

# Create an ArgumentParser with a list of desired Command line parameters

parser = argparse.ArgumentParser()
parser.add_argument('--config', default=default_config_file)
parser.add_argument('--PORT', action=EnvDefault, envvar='PORT', required=False)
parser.add_argument('--BASEURL', action=EnvDefault, envvar='BASEURL', required=False)
parser.add_argument('--ECISURL', action=EnvDefault, envvar='ECISURL', required=False)
parser.add_argument('--ADMIN_BASEURL', action=EnvDefault, envvar='ADMIN_BASEURL', required=False)
parser.add_argument('--HEARTBEAT_URL', action=EnvDefault, envvar='HEARTBEAT_URL', required=False)
parser.add_argument('--RABBITMQ_URL', action=EnvDefault, envvar='RABBITMQ_URL', required=False)
parser.add_argument('--CREDENTIALS', action=EnvDefault, envvar='CREDENTIALS', required=False)
parser.add_argument('--SECURITY_AUTHTYPE', action=EnvDefault, envvar='SECURITY_AUTHTYPE', required=False)
parser.add_argument('--NODENAME', action=EnvDefault, envvar='NODENAME', required=False)
parser.add_argument('--CREATING_SYSTEM_ID', action=EnvDefault, envvar='CREATING_SYSTEM_ID', required=False)
parser.add_argument('--CONTROL_MODE', action=EnvDefault, envvar='CONTROL_MODE', required=False)
parser.add_argument('--SUT', action=EnvDefault, envvar='SUT', required=False)

def get_variables():
    '''
    Fetches and passes along environment-specific variables using the following priority:
    1. Command Line Arguments
    2. Environment Variables
    3. Configuration file (from the INI file specified using the --config argument)
    '''

    # Parse args to get chosen config file for ConfigParser
    args, unknown = parser.parse_known_args()

    config = configparser.ConfigParser()
    config.optionxform = str # Allow parsed keys to be uppercase
    config.read(args.config)

    result = dict(config['ENVIRONMENT'])
    result['CREDENTIALS'] = dict(config['CREDENTIALS'])
    result['AUTHORIZATION'] = dict(config['AUTHORIZATION'])
    result['OAUTH_ACCESS_GRANT'] = dict(config['OAUTH_ACCESS_GRANT'])
    result[result['SUT']] = dict(config['SUT'])
    result[result['SUT']]['CREDENTIALS'] = dict(config['SUT.CREDENTIALS'])
    # TODO: what else is needed to support everything?

    # Overwrite anything from Environment variables or Command parameters to final result
    args = vars(args)
    result.update({k: v for k, v in args.items() if v is not None})

    return result

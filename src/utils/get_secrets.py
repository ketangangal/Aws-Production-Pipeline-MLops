import os
import json

def secrets(ENV_VAR = 'AWS_SECRETS'):
    SECRETS = os.environ.get(ENV_VAR)
    print(SECRETS)
    return json.loads(SECRETS)

if __name__ == '__main__':
    secrets()
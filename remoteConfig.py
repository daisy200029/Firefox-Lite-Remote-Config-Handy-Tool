import argparse
import requests
import io
from oauth2client.service_account import ServiceAccountCredentials

BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

ENVS_INFO = {
    "nightly": {"PROJECT_ID": "rocketnightly",
                "KEY_FILE": "service-account-nightly.json"},
    "prod":
    {"PROJECT_ID": "zerda-dcf76",
     "KEY_FILE": "service-account-prod.json"}}


def _set_env(env):
    """Retrieve project infomation of target environment
    Args:
      env: user input environment key

    """
    if env in ENVS_INFO:
        global PROJECT_ID, KEY_FILE, REMOTE_CONFIG_ENDPOINT, REMOTE_CONFIG_URL
        PROJECT_ID = ENVS_INFO[env]["PROJECT_ID"]
        KEY_FILE = ENVS_INFO[env]["KEY_FILE"]
        REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
        REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
        print('tartget project_id is : ', PROJECT_ID)
        print('tartget key_file is : ', KEY_FILE)

# [START retrieve_access_token]


def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE, SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token
# [END retrieve_access_token]


def _get(env):
    """Retrieve the current Firebase Remote Config template from server.

    Retrieve the current Firebase Remote Config template from server and store it

    locally.
    """
    _set_env(env)

    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }
    resp = requests.get(REMOTE_CONFIG_URL, headers=headers)

    if resp.status_code == 200:
        with io.open('config_{}.json'.format(env), 'wb') as f:
            f.write(resp.text.encode('utf-8'))

        print('Retrieved template has been written to config_{}.json'.format(env))
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Unable to get template')
        print(resp.text)


def _listVersions(env):
    """Print the last 5 Remote Config version's metadata."""

    _set_env(env)
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }
    resp = requests.get(
        REMOTE_CONFIG_URL +
        ':listVersions?pageSize=5',
        headers=headers)

    if resp.status_code == 200:
        print('Versions:')
        print(resp.text)
    else:
        print('Request to print template versions failed.')
        print(resp.text)


def _rollback(env, version):
    """Roll back to an available version of Firebase Remote Config template.

    :param version: The version of the template to roll back to.
    """
    _set_env(env)
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }

    json = {
        "version_number": version
    }
    resp = requests.post(
        REMOTE_CONFIG_URL +
        ':rollback',
        headers=headers,
        json=json)

    if resp.status_code == 200:
        print('Rolled back to version: ' + version)
        print(resp.text)
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Request to roll back to version ' + version + ' failed.')
        print(resp.text)


def _publish(env, etag):
    """Publish local template to Firebase server.

    Args:
      etag: ETag for safe (avoid race conditions) template updates.
          * can be used to force template replacement.
    """
    _set_env(env)
    with open('config_{}.json'.format(env), 'r', encoding='utf-8') as f:
        content = f.read()
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
        'If-Match': etag
    }
    resp = requests.put(
        REMOTE_CONFIG_URL,
        data=content.encode('utf-8'),
        headers=headers)
    if resp.status_code == 200:
        print('Template has been published.')
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Unable to publish template.')
        print(resp.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--env',
        required=True,
        help='env can be "nightly"or "prod"')
    parser.add_argument('--action')
    parser.add_argument('--etag')
    parser.add_argument('--version')
    args = parser.parse_args()

    if args.action and args.action == 'get' and args.env:
        _get(args.env)
    elif args.action and args.action == 'publish' and args.etag and args.env:
        _publish(args.env, args.etag)
    elif args.action and args.action == 'versions' and args.env:
        _listVersions(args.env)
    elif args.action and args.action == 'rollback' and args.version and args.env:
        _rollback(args.env, args.version)
    else:
        print('''Invalid command. Please use one of the following commands:
python3 remoteConfig.py --action=get --env=nightly
python3 remoteConfig.py --action=publish --env=nightly --etag=<LATEST_ETAG>
python3 remoteConfig.py --action=versions --env=nightly
python3 remoteConfig.py --action=rollback --env=nightly --version=<TEMPLATE_VERSION_NUMBER>''')


if __name__ == '__main__':
    main()

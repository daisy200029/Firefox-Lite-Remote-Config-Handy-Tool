# Firefox Lite Remote Config Handy Tool

 This script can 1)retrieve, 2)publish, 3)rollback version 4)list versions of Firebase remote configuration on [FirefoxLite Preview](https://console.firebase.google.com/u/0/project/rocketnightly/config) or [FirefoxLite Production](https://console.firebase.google.com/u/0/project/zerda-dcf76/config) projects.

## Prerequisition
1. Download admin private key from Firefox Nightly and Firefox Prod Firebase settings , refer [get access token](https://firebase.google.com/docs/remote-config/use-config-rest)
2. After download Nightly key, please place in the same folder and reanme it to "service-account-nightly.json"
3. After download Production key, please place in the same folder and reanme it to "service-account-prod.json"

## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install Remote Config Script.

```bash
pip3 install -r requirements.txt
```

## Usage
 
Please use one of the following commands:

```bash
python3 remoteConfig.py --action=get --env=<prod|nightly>
python3 remoteConfig.py --action=publish --env=<prod|nightly> --etag=<LATEST_ETAG>
python3 remoteConfig.py --action=versions --env=<prod|nightly>
python3 remoteConfig.py --action=rollback --env=<prod|nightly> --version=<TEMPLATE_VERSION_NUMBER>
```
## Authors

* **[Daisy Liu](https://github.com/Daisy-pliu)** 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


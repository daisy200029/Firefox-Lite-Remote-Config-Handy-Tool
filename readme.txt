# Firefox Lite Remote Config Handy Tool

This script can be used to get/publish/rollback Firebase remote configuration on either [FirefoxLite Preview](https://console.firebase.google.com/u/0/project/rocketnightly/config) or [Production](https://console.firebase.google.com/u/0/project/zerda-dcf76/config) remote config 

## Prerequisition
1. Download admin private key from Firebase settings, refer [get access token](https://firebase.google.com/docs/remote-config/use-config-rest)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Remote Config Script.

```bash
pip3 install requirements.txt
```

## Usage
 
Please use one of the following commands:

```python
python3 remoteConfig.py --action=get --env=<prod|nightly>
python3 remoteConfig.py --action=publish --env=nightly --etag=<LATEST_ETAG>
python3 remoteConfig.py --action=versions --env=<prod|nightly>
python3 remoteConfig.py --action=rollback --env=<prod|nightly> --version=<TEMPLATE_VERSION_NUMBER>
```
## Authors

* **[Daisy Liu](https://github.com/Daisy-pliu)** 
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


# Steam TOTP

This library generates Steam-style 5-digit alphanumeric two-factor authentication codes given a shared secret.

Works on Python >3.6,<4.0, may work on Python 2.7.x but not tested.

## Usage

### Install
You can install from PyPi.

```bash
❯ pip install steam-totp
```

Or install from GitHub for latest version.

```bash
❯ pip install https://github.com/shabbywu/python-steam-totp/archive/main.zip
```

### Examples
```python
from steam_totp import generate_twofactor_code_for_time

code = generate_twofactor_code_for_time(shared_secret="your-shared-secret")
```

# yyy-photo-bot
A [Twitter bot](https://twitter.com/yyy_photo_bot) for tweeting Readyyy's CG artwork.

# Configuration
Make sure you mount the directory where the CG are located correctly~

The files should be named something like `img_card_chara_m_aki_0016_1.png`

And this is how the directory should look like:
```shell
PhotoIllust
├── !Border
│   ├── Medium
│   └── Small
├── Aki
│   ├── Large
│   ├── Medium
│   └── Small
├── Ango
│   ├── Large
│   ├── Medium
│   └── Small
├── Azusa
│   ├── Large
...
```

And oh, you also need to make a `config.py` like this:
(`photo_queue` is a deque of `Card.id` from CardData.json that you want to tweet)
(`file_prefix` is for getting the right filename, defaults to `''`)
(`illustration_path` is path-like object of the root of the CG folder like above)
(`report` is a function to report errors that happens)
```python
from collections import deque
from pathlib import Path
API_KEY = "your twitter api key"
API_SECRET = "your twitter api secret"
ACCESS_TOKEN = "your twitter access token"
ACCESS_SECRET = "your twitter access secret"
illustration_path = Path('/app/PhotoIllust')
file_prefix = ''
photo_queue = deque()

def report(error):
    print(error)
```

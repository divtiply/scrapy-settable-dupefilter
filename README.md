# Scrapy Settable DupeFilter

## Usage

Add following to the project `settings.py`:

```python
DUPEFILTER_CLASS = 'scrapy_settable_dupefilter.SettableRFPDupeFilter'
```

A request can be set as seen by providing `seen_request=True` within request meta.
Seen requests and all subsequent request to the same resource are filtered out.

It is also possible to populate dupefilter seen requests from file:

```python
from scrapy_settable_dupefilter import set_seen_requests_from

def start_requests(self):
    seen_urls = 'urllist.txt'
    set_seen_requests_from(seen_urls)
    super().start_requests()
```

# Scrapy Settable DupeFilter

## Usage

Add following to the project `settings.py`:

    DUPEFILTER_CLASS = 'scrapy_settable_dupefilter.SettableRFPDupeFilter'

Any request can be set as seen with `seen_request` request meta.
Seen requests and all subsequent request to the same resource are filtered out.

It is possible to populate dupefilter seen requests from file:

    from scrapy_settable_dupefilter import set_seen_requests_from

    def start_requests(self):
        seen_urls = 'urllist.txt'
        set_seen_requests_from(seen_urls)
        super().start_requests()

## License

MIT

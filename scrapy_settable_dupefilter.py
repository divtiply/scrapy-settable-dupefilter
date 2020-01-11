import json
from scrapy.dupefilters import RFPDupeFilter
from scrapy import Request
from scrapy.utils.request import referer_str


class SettableRFPDupeFilter(RFPDupeFilter):
    
    def __init__(self, *args, **kwargs):
        super(SettableRFPDupeFilter, self).__init__(*args, **kwargs)
        self.logsetseen = True

    def request_seen(self, request):
        return (
            super(SettableRFPDupeFilter, self).request_seen(request)
            or request.meta.get('request_seen'))

    def log(self, request, spider):
        if request.meta.get('request_seen') == None:
            return super(SettableRFPDupeFilter, self).log(request, spider)
        if self.debug:
            msg = "Set request seen: %(request)s (referer: %(referer)s)"
            args = {'request': request, 'referer': referer_str(request) }
            self.logger.debug(msg, args, extra={'spider': spider})
        elif self.logsetseen:
            msg = ("Set request seen: %(request)s"
                   " - no more set seen duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logsetseen = False

        spider.crawler.stats.inc_value('dupefilter/set_seen', spider=spider)


def make_seen_request_from_url(url, **kwargs):
    return Request(url, lambda: None, meta=dict(request_seen=True), **kwargs)


def set_seen_requests_from(filepath, urlfield='url', filetype=None):
    if not filetype:
        if any(
            filepath.endswith(ext)
            for ext in ('.jl', '.jsonl', '.jsonlines')
        ):
            filetype = 'jsonlines'
    
    with open(filepath, encoding='utf-8') as f:
        if filetype == 'jsonlines':
            for line in f:
                json_line = json.loads(line)
                url = json_line[urlfield]
                yield make_seen_request_from_url(url)
        else:  # text, one url per line
            for url in f:
                yield make_seen_request_from_url(url)

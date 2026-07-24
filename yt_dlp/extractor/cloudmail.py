from .common import InfoExtractor
import base64

class CloudMailIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?cloud\.mail\.ru/public/(?P<id>[\w-]+/[\w-]+)'
    _TESTS = [{
        'url': 'https://yourextractor.com/watch/42',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            # For videos, only the 'id' and 'ext' fields are required to RUN the test:
            'id': '42',
            'ext': 'mp4',
            # Then if the test run fails, it will output the missing/incorrect fields.
            # Properties can be added as:
            # * A value, e.g.
            #     'title': 'Video title goes here',
            # * MD5 checksum; start the string with 'md5:', e.g.
            #     'description': 'md5:098f6bcd4621d373cade4e832627b4f6',
            # * A regular expression; start the string with 're:', e.g.
            #     'thumbnail': r're:https?://.*\.jpg$',
            # * A count of elements in a list; start the string with 'count:', e.g.
            #     'tags': 'count:10',
            # * Any Python type, e.g.
            #     'view_count': int,
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        slug = base64.b64encode(video_id.encode('utf-8')).decode('utf-8')
        webpage = self._download_webpage(url, video_id)
        source_url = self._html_search_regex(r'"(https?://[^"]*videowl[^"]*)"', webpage, 'cloudSettings')
        m3u8 = f"{source_url}/0p/{slug}.m3u8?double_encode=1"
        formats = self._extract_m3u8_formats(m3u8, '', 'mp4', 'm3u8_native', m3u8_id='hls', fatal=False)
        title = self._og_search_property("title", webpage)
        description = self._og_search_property("description", webpage)

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'formats': formats,
        }

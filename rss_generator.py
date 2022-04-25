#!/usr/bin/env python3

class RssGenerator:
    def __init__(self):
        pass

    @staticmethod
    def format_timestamp(t):
        DoW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        result = DoW[int(t.strftime('%w'))]
        result += ', '
        result += t.strftime('%d %b %Y %H:%M:%S')
        result += ' +0000'
        return result

    @staticmethod
    def generate(options, file_list):
        result = ''
        title = 'Media files from {0}'.format(options.bucket_name)
        result += """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podaccess="https://access.acast.com/schema/1.0/" version="2.0">
<channel>
<title>{title}</title>
<link>{link}</link>
{blockitunes}
<language>en-us</language>""".format(
            title=title,
            link=options.base_url,
            blockitunes=('<itunes:block>yes</itunes:block>' if options.private else ''),)
        for f in file_list:
            result += """<item>
    <title>{filename}</title>
    <description>{filename}</description>
    {blockitunes}
    <link>{link}</link>
    <enclosure url="{media_link}" type="audio/mpeg" length="{size}"></enclosure>
    <pubDate>{pubdate}</pubDate>
    <guid>{filename}</guid>
    {premium}
</item> 
""".format(
                filename=f.filename,
                blockitunes=('<itunes:block>yes</itunes:block>' if options.private else ''),
                link=options.base_url,
                media_link=options.base_url + f.filename,
                pubdate=RssGenerator.format_timestamp(f.modified),
                size=f.size,
                premium=('<podaccess:premium locked="true"/>' if options.private else '')
            )

        result += '</channel></rss>'
        return result

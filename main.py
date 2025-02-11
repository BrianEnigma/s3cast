#!/usr/bin/env python3

import boto3
import botocore.exceptions
import datetime
import pprint
import random
import time
from arguments import *
from file_fetcher import *
from rss_generator import *


def get_bucket_website(client, bucket_name):
    try:
        settings = client.get_bucket_location(Bucket=bucket_name)
        location = settings['LocationConstraint']
        if location is None or len(location) == 0:
            raise RuntimeError('Unable to get bucket location')
        return 'http://{bucket}.s3-website-{region}.amazonaws.com/'.format(bucket=bucket_name, region = location)
    except botocore.exceptions.ClientError as e:
        raise RuntimeError('Error getting bucket website configuration: {0}'.format(str(e)))


def swizzle_list(options, file_list):
    result = file_list

    # Randomize the list, if asked for.
    if options.random:
        random.shuffle(result)
    if options.sort_by_name:
        result.sort(key=(lambda item : item.filename))
        item_time = datetime.datetime(2022, 1, 1, 0, 0).timestamp()
        for item in result:
            item.modified = datetime.datetime.fromtimestamp(item_time)
            item_time += 60 * 60 * 24
    elif not options.random:
        result.sort(key=(lambda item: item.modified))
    # Trim list to length, if a limit was asked for.
    if 0 < options.limit < len(result):
        new_list = result[(-1 * options.limit):]
        result = new_list
    return result


def main():
    parser = ParseArguments()
    options = parser.parse()
    if options.profile:
        session = boto3.Session(profile_name=options.profile)
        s3 = session.client('s3')
    else:
        s3 = boto3.client('s3')
    try:
        options.base_url = get_bucket_website(s3, options.bucket_name)
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)
    file_fetcher = FileFetcher()
    file_fetcher.do_fetch(s3, options.bucket_name, options.infer_date)
    file_list = file_fetcher.get_file_list()
    description_dictionary = file_fetcher.get_description_dictionary()
    cover_image = file_fetcher.get_cover_image()
    new_list = swizzle_list(options, file_list)
    file_list = new_list
    #pprint.pprint(description_dictionary)
    #print('')
    #print('')
    #print('')
    #for f in file_list:
    #    print(f)
    rss_text = RssGenerator.generate(options, file_list, description_dictionary, cover_image)
    if options.dry_run:
        print(rss_text)
    else:
        s3.put_object(
            Bucket=options.bucket_name,
            Key='{0}.xml'.format(options.index_name),
            Body=rss_text
        )
    m3u8_text = RssGenerator.generate_m3u8(options, file_list, cover_image)
    if options.dry_run:
        print(m3u8_text)
    else:
        s3.put_object(
            Bucket=options.bucket_name,
            Key='{0}.m3u8'.format(options.index_name),
            ContentType='application/x-mpegURL',
            Body=m3u8_text
        )
    if options.index_name == 'index':
        player_text = RssGenerator.generate_player(options, file_list, description_dictionary, cover_image)
        if options.dry_run:
            print(player_text)
        else:
            s3.put_object(
                Bucket=options.bucket_name,
                Key='player.html',
                ContentType='text/html',
                Body=player_text
            )


if __name__ == '__main__':
    random.seed()
    main()

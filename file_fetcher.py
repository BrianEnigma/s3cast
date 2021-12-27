#!/usr/bin/env python3

import boto3


class MediaFile:
    def __init__(self):
        self.filename = None
        self.modified = None
        self.size = 0

    def __str__(self):
        return '{0} {1} {2}'.format(self.filename, self.size, self.modified)


class FileFetcher:
    def __init__(self):
        pass

    @staticmethod
    def is_wanted_file(filename):
        return filename.endswith('.mp3')

    @staticmethod
    def fetch(client, bucket_name):
        result = []
        response = client.list_objects_v2(
            Bucket=bucket_name
        )
        for item in response['Contents']:
            file = MediaFile()
            file.filename = item['Key']
            file.modified = item['LastModified']
            file.size = item['Size']
            if FileFetcher.is_wanted_file(file.filename):
                result.append(file)
        return result

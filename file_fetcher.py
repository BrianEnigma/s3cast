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
        self._file_list = []
        self.cover_image = None

    @staticmethod
    def is_media_file(filename):
        return filename.endswith('.mp3')

    @staticmethod
    def is_cover_image_file(filename):
        return filename == 'cover.jpg'

    def fetch(self, client, bucket_name):
        self._file_list = []
        response = client.list_objects_v2(
            Bucket=bucket_name
        )
        for item in response['Contents']:
            file = MediaFile()
            file.filename = item['Key']
            file.modified = item['LastModified']
            file.size = item['Size']
            if FileFetcher.is_media_file(file.filename):
                self._file_list.append(file)
            if FileFetcher.is_cover_image_file(file.filename):
                self.cover_image = file.filename
        return self._file_list

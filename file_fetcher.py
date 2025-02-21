#!/usr/bin/env python3

import boto3
import datetime
import re


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
        self._description_list = {}
        self._cover_image = None
        self._date_matcher = re.compile(r'.*([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]).*')

    @staticmethod
    def is_media_file(filename):
        return filename.endswith('.mp3') or filename.endswith('.m4a')

    @staticmethod
    def is_description_file(filename):
        return filename.endswith('.txt')

    @staticmethod
    def is_cover_image_file(filename):
        return filename == 'cover.jpg'

    def get_file_list(self):
        return self._file_list

    def get_description_dictionary(self):
        return self._description_list

    def get_cover_image(self):
        return self._cover_image

    def _extract_date(self, filename:str) -> datetime.datetime:
        result = None
        matches = self._date_matcher.match(filename)
        if matches is not None:
            result = datetime.datetime(
                int(matches.group(1)[0:4]),
                int(matches.group(1)[4:6]),
                int(matches.group(1)[6:8]))
        return result

    # def _fetch_content(self, client, bucket_name, filename):
    #     s3_object = client.Object(bucket_name, filename)
    #     body = s3_object['Body']
    #     return body.read()

    def do_fetch(self, client, bucket_name:str, infer_dates:bool):
        self._file_list = []
        response = client.list_objects_v2(
            Bucket=bucket_name
        )
        for item in response['Contents']:
            file = MediaFile()
            file.filename = item['Key']
            file.modified = item['LastModified']
            if infer_dates:
                extracted_date = self._extract_date(file.filename)
                if extracted_date is not None:
                    file.modified = extracted_date
            file.size = item['Size']
            if FileFetcher.is_media_file(file.filename):
                self._file_list.append(file)
            elif FileFetcher.is_description_file(file.filename):
                corresponding_media_name = re.sub('txt$', 'mp3', file.filename)
                self._description_list[corresponding_media_name] = client.get_object(Bucket=bucket_name, Key=file.filename)['Body'].read().decode('UTF-8')
            elif FileFetcher.is_cover_image_file(file.filename):
                self._cover_image = file.filename

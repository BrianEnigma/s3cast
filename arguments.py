#!/usr/bin/env python3

import argparse
import sys

class ProgramOptions:
    def __init__(self):
        self.random = False
        self.sort_by_name = False
        self.limit = 0
        self.profile = None
        self.bucket_name = None
        self.base_url = None
        self.dry_run = False
        self.private = True

    def __str__(self):
        result = ''
        result += "random={0}\n".format(self.random)
        result += "limit={0}\n".format(self.limit)
        result += "profile={0}\n".format(self.profile)
        result += "bucket_name={0}\n".format(self.bucket_name)
        result += "base_url={0}\n".format(self.base_url)
        result += "private={0}\n".format(self.private)
        result += "dry_run={0}\n".format(self.dry_run)
        return result

class ParseArguments:
    def __init__(self):
        self._program_options = ProgramOptions()

    def parse(self):
        result = ProgramOptions()

        # Set up args
        parser = argparse.ArgumentParser(description='Turn an S3 bucket of mp3 files into a podcast RSS feed.')

        group = parser.add_argument_group(title='AWS Options', description='Arguments related to S3 access.')
        group.add_argument('--profile', dest='profile', action='store', required=False,
                            help='aws-cli profile name to use')
        group.add_argument('--bucket', dest='bucket', action='store', required=True,
                            help='S3 bucket to use')

        group = parser.add_argument_group(title='Publishing', description='Arguments related to publishing.')
        group.add_argument('--private', dest='private', action='store_true', help='Whether to tag the RSS as public/private (default is private)')
        group.add_argument('--public', dest='public', action='store_true', help='Whether to tag the RSS as public/private (default is private)')

        group = parser.add_argument_group(title='Selection', description='Arguments related to selecting files.')
        group.add_argument('--limit', dest='limit', action='store', help='Maximum number of files to include')
        group.add_argument('--random', dest='random', action='store_true', help='Whether to randomize the order')
        group.add_argument('--sort-by-name', dest='sort_by_name', action='store_true', help='Whether to sort the files by filename')

        group = parser.add_argument_group(title='Testing', description='Arguments related to testing.')
        group.add_argument('--dry-run', dest='dry_run', action='store_true', help='Only print the RSS file, do not upload it')

        # Parse them
        args = parser.parse_args()

        # Validate
        if args.random and args.sort_by_name:
            raise RuntimeError('Cannot randomize and sort at the same time.')
        if args.private and args.public:
            raise RuntimeError('Cannot be public and private at the same time.')

        # Copy in arguments
        if args.profile:
            result.profile = args.profile
        if args.bucket:
            result.bucket_name = args.bucket
        if args.limit:
            result.limit = int(args.limit)
        if args.random:
            result.random = True
        if args.sort_by_name:
            result.sort_by_name = True
        if args.dry_run:
            result.dry_run = True
        result.private = True
        if args.public:
            result.private = False

        # Check for errors
        if args.bucket is None or len(args.bucket) == 0:
            result = None
            parser.error('A bucket name is required')

        return result


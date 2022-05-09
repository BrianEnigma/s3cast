# s3cast

## Purpose

With [s3cast](https://github.com/BrianEnigma/s3cast), you can take an s3 bucket full of MP3 files and generate a simple RSS file that is compatible with most podcast players.

I occasionally record radio shows that not streamable online. From this, I have a whole collection of MP3 files that I'd like to be easily accessible from my phone and tablet. This is totally possible by copying the files directly to the device, but sync would be nice. You can sync them through a service like Dropbox, but these files are multiple hours long, and it would be nice for a player to remember where I was when playing a file. Podcast players are perfect for this sort of task, but I really didn't want to hand-craft the RSS XML to wrap these files. 

This script fills that need. I can upload each new MP3 file to a bucket. Running the script, pointed to that bucket, it will generate a podcast RSS XML and save that as `index.xml` in that bucket. There are a few options to limit the feed to the last _n_ items, as well as shuffle them.

## License

This software is written and maintained by me, [Brian Enigma](https://github.com/BrianEnigma). It is copyright 2021 and is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

## Prerequisites

- Python
- The boto3 Python package
- The `aws` client application
- An S3 bucket...
    - ...that you've set up
    - ...that you've uploaded some MP3 files to
    - ...that you've enabled static website hosting on (this is under “Properties”)

## Setup

Of course, you will need an S3 bucket with your MP3 media files on it. Part of setting up and accessing that S3 bucket is the AWS permissions. There will be an AWS Access Key ID and an AWS Secret Access Key. You probably had to use them to set up your file transfer application. If they are not already set up in the `aws` CLI program, then you will need to configure it — otherwise you can skip the `aws configure` step.

This is a Python application. It needs the `boto3` package installed, as well as the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) command line app. You'll need to set up credentials with the `aws` client.

The simplest way to do this on a Mac with [homebrew](https://brew.sh) installed is:

```
brew install awscli
aws configure
pip3 install boto3
```

A more advanced user might choose to use “profiles” to better compartmentalize permissions and access. Both the AWS client and s3cast allow for a `--profile` flag. For example:

```
aws configure --profile podcasting
pip3 install boto3
./s3cast --profile podcasting --bucket my_bucket_name
```

## Usage

In its simplest form, s3cast can be run with just a bucket name:

```
./main.py --bucket my_podcast_bucket
```

This will use your default AWS client permissions to look at the files within `my_podcast_bucket`, locate the MP3 files, generate a podcast XMLs, then upload that file to the root of the bucket as `index.xml`. It will also upload an `index.m3u8` with the list of media files as well as `player.html` that acts as a basic JavaScript browser player.

If you have a file in the bucket named `cover.jpg`, then it will be used as the “cover artwork.”

Other options are available:

- `--profile` will select a specific AWS CLI profile, instead of the default one.
- `--limit {number}` will limit the RSS feed to only the last `{number}` files it sees in the bucket.
- `--random` will shuffle the order of the files in the RSS feed.
- `--dry-run` will perform all actions up to (and including) generating the content of the RSS feed. Instead of uploading it as `index.xml` to the bucket, it will simply print out the file contents.

When using `random` and `limit` at the same time, the shuffling will occur first, followed by limiting the RSS item count.

## Limits

- The particular AWS API I'm using (`list_objects_v2`) is limited to 1,000 items in the bucket in the mode that I'm using it. The API itself has a way to fetch more, but that is not actively implemented in this code.


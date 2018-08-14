import errno
import os
from time import time
from math import ceil
from multiprocessing.pool import ThreadPool
from botocore.client import Config
import boto3
import logging

#python2 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

# Log to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamformater = logging.Formatter("[%(levelname)s] %(message)s")

logstreamhandler = logging.StreamHandler()
logstreamhandler.setLevel(logging.INFO)
logstreamhandler.setFormatter(streamformater)
logger.addHandler(logstreamhandler)

class S3Uploader(object):
    """
    Used to upload entire filders to S3 bucket.
    python2 and python3 compatible.
    """

    def __init__(self, aws_access_key_id = None, aws_secret_access_key = None, aws_session_token = None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        if aws_access_key_id and aws_access_key_id:
            logger.info("Initializing session for user: {}".format(aws_access_key_id))
            self.s3 = self._init_session()

    def _init_session(self):
        """ in case we want to initialize the session manually """
        session = boto3.session.Session(aws_access_key_id=self.aws_access_key_id,
                                        aws_secret_access_key=self.aws_secret_access_key,
                                        aws_session_token=self.aws_session_token,
                                        )
        config = Config(connect_timeout=5, read_timeout=5)
        return session.resource('s3', config=config)

    def get_buckets(self):
        """
        returns list of all buckets, that the user has access to
        :return: list()
        """
        return [s3bucket.name for s3bucket in self.s3.buckets.all()]

    def print_buckets(self):
        """
        prints all buckets, that the user has access to
        :return:
        """
        print("Available buckets:")
        for n, bucket in enumerate(self.s3.buckets.all()):
            print("{number}: {name}".format(number=n, name=bucket.name))

    @classmethod
    def check_path(cls, path):
        """
        self-explainatory

        :param path: local path
        :type path: str
        :return: valid path
        """
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
        return path

    def _validate_bucket(self, bucketName):
        """
        self-explainatory.
        By default there is no check if the supplied bucket name is valid or not.
        This method ensures, that the bucketName provided exists.

        :param bucketName: Name of s3 bucket
        :type bucketName: str
        :return: valid s3.Bucket object
        """
        assert bucketName in self.get_buckets(), "s3 bucket provided was not found."
        return self.s3.Bucket(bucketName)

    def upload_dir(self, localPath, remotePath, bucketName, threads=10):
        """
        Upload local directory to s3 bucket with prefix(remote path).

        :param localPath: Local directory or file path
        :param remotePath: Remote prefix
        :param bucketName: bucket name with create object permissions
        :param threads: number of threads.
        :type localPath: str
        :type remotePath: str
        :type bucketName: str
        :type threads: int
        :return: (float) Elapsed time in seconds.
        """

        def __buildFileList(local_dir_path):
            """
            Creates list of files

            :param local_dir_path: local directory path
            :type local_dir_path: str
            :return: list
            """
            filelist = []
            for root, dirs, files in os.walk(local_dir_path, topdown=False):
                for name in files:
                    filelist.append(str(os.path.join(root, name)))
            return filelist

        def __mp_upload_to_bucket(filename):
            """
            multiprocessing safe upload func

            :rtype: None
            :param filename: full path to local file
            :return:
            """
            logger.info('Uploading {}'.format(filename))
            if os.name == 'nt':
                bucket.upload_file(filename,
                                   remotePath + filename.replace(local_dir_path + '\\', '').replace('\\', '/'))
            else:
                bucket.upload_file(filename, remotePath + filename.replace(local_dir_path + '/', ''))

        assert remotePath, "remote path can't be empty!"
        assert localPath, "local directory path can't be empty!"

        # this is required in order not to break path
        if not remotePath.endswith('/'):
            remotePath += '/'

        # local path normalize
        local_dir_path = self.check_path(localPath.replace('\\','/'))

        # generate list of files
        filelist = __buildFileList(local_dir_path)

        # validate bucket bucket
        bucket = self._validate_bucket(bucketName)

        start_time = time()
        # some smart threading
        pool = ThreadPool(processes=threads if ceil(len(filelist) / 10) < threads else ceil(len(filelist) / 10))
        pool.map(__mp_upload_to_bucket, filelist)
        stop_time = time()

        #return elapsed time
        return(stop_time - start_time)


    def list_bucket_files(self, bucketName, filter=None, limit=None):
        """
        List files in given bucket. filter prefix can (and shuold) be used.

        :param bucketName: Name of the s3 bucket
        :type bucketName: s3.Bucket
        :param filter: Filter prefix. Needed if you miss permissions to list all objects in the given bucket.
        :type filter: str
        :param limit: Limit the results to a given number.
        :type limit: int
        :return: None
        """
        bucket = self._validate_bucket(bucketName)
        print('Files in bucket {} filtered by {}:'.format(bucketName, filter))
        for key in bucket.objects.filter(Prefix=filter).limit(count=limit):
            print("{} {:16} {}".format(key.last_modified, key.size, key.key))


def main():

    #Grizmin.org
    aws_access_key_id = 'AKIAIF5XHF5OSQTLTVFQ'
    aws_secret_access_key = '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'

    a = S3Uploader(aws_access_key_id, aws_secret_access_key)

    a.upload_dir('c:/temp', 'some/long/path', 'grizmin-test')
    a.list_bucket_files('grizmin-test')
    
    logger.info("Upload took {0:.2f} seconds.".format(upload_time))

if __name__ == '__main__':
    main()

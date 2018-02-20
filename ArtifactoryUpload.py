#!/usr/bin/env python3

import sys
import subprocess
import datetime
import argparse
import logging
import time

# Log to stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
streamformater = logging.Formatter("[%(levelname)s] %(message)s")

logstreamhandler = logging.StreamHandler()
logstreamhandler.setLevel(logging.INFO)
logstreamhandler.setFormatter(streamformater)
logger.addHandler(logstreamhandler)


class RunCommand:
    """ Safe run command """
    allowed_commands = ['jfrog']

    def __init__(self, command):
        self.command = command
        self.time_taken = 0

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, cmd):
        """ assert that command is in allowed_commands """
        try:
            assert cmd.split()[0] in self.allowed_commands, 'illegal command. allowed_commands: {}'.format(
                self.allowed_commands)
        except AssertionError:
            print('illegal command. allowed_commands: {}'.format(self.allowed_commands))
            exit(1)
        self._command = cmd

    def run(self, timeout = 300):
        """ Runs the command.
            :sets time_taken
            :returns command exit code
        """

        command = self.command.split()
        # c = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        start = time.time()
        try:
            return_code = subprocess.call(command, timeout=timeout)
        except subprocess.TimeoutExpired:
            logger.error("Timeout reached. Subprocess killed.")
            return_code = 1

        stop = time.time()
        self.time_taken = stop - start
        return return_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_version', '-bv', help='build version. Eg. \'18.3.0.95\n\'', required=True)
    arg = parser.parse_args()

    # version magic
    verarr = arg.build_version.split('.')
    assert len(verarr) == 4, "Invalid version: {}".format(arg.build_version)
    major_version = '.'.join(verarr[:2])
    minor_version = '.'.join(verarr[2:])

    cmd = "jfrog rt upload --threads=16\
 /dserver/poker/{build_version_major}/{build_version_minor}/(*)/*\
 generic-poker-snapshot-local/{build_version_major}/{build_version_minor}/{{1}}/".format(
        build_version_major=major_version, build_version_minor=minor_version, build_version=arg.build_version
    )
    upload_command = RunCommand(cmd)
    exit_code = upload_command.run(timeout=60)
    if exit_code:
        logger.error("[!] Upload failed.")
        exit(exit_code)
    else:
        logger.info("[*] Files were uploaded successfully for {:.3} seconds.".format(upload_command.time_taken))


if __name__ == '__main__':
    logger.info("Starting {} on {} with params: {}".format(sys.argv[0],
                                                           datetime.datetime.today(), sys.argv[1:]))
    main()

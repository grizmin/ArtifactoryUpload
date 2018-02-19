#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime
import argparse
import logging
import shlex

# Log to stdout
logger = logging.getLogger(__name__)

streamformater = logging.Formatter("%(levelname)s:  %(message)s")

logstreamhandler = logging.StreamHandler()
logstreamhandler.setLevel(logging.INFO)
logstreamhandler.setFormatter(streamformater)
logger.addHandler(logstreamhandler)

class RunCommand():
    allowed_commands = ['jfrog']
    def __init__(self, command):
        self.command = command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, cmd):
        try:
            assert cmd.split()[0] in self.allowed_commands, 'illegal command. allowed_commands: {}'.format(self.allowed_commands)
        except AssertionError:
            print('illegal command. allowed_commands: {}'.format(self.allowed_commands))
            exit(1)
        self._command = cmd

    def run(self):
        command = self.command.split()
        # c = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        subprocess.call(command,shell=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_version', '-bv', help='build version. Eg. \'18.3.0.95\n\'', required=True)
    arg = parser.parse_args()

    # version magic
    verarr = arg.build_version.split('.')
    assert len(verarr) == 4
    major_version = '.'.join(verarr[:2])
    minor_version = '.'.join(verarr[2:])

    print(major_version, minor_version)
    print('executing: ./command {}'.format(arg.build_version))
    cmd = "jfrog rt upload --threads=16\
            --build-number={build_version} /dserver/poker/{build_version_major}/{build_version_minor}/\(*\)/*\
             generic-poker-snapshot-local/{build_version_major}/{build_version_minor}/\{1\}/".format(
        build_version_major=major_version, build_version_minor=minor_version, build_version=arg.build_version
    )
    print(cmd)
    c1 = RunCommand(cmd)
    c1.run()


if __name__ == '__main__':
    logger.info("Starting {} on {} with params: {}".format(sys.argv[0],
                                                           datetime.datetime.today(), sys.argv[1:]))
    main()
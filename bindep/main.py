# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import optparse
import os.path
import sys

import bindep.depends


logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(message)s")


def _split_constraint(constraint):
    return constraint.rsplit('=', 1)


def main(depends=None):
    usage = "Usage: %prog [options] [profile]"
    parser = optparse.OptionParser(
        usage=usage, version="%%prog %s" % bindep.version)
    parser.add_option(
        "-b", "--brief", action="store_true", dest="brief",
        help="List only missing packages one per line.")
    parser.add_option(
        "-f", "--file", action="store", type="string", dest="filename",
        default="",
        help="Package list file (default: bindep.txt or "
             "other-requirements.txt).")
    parser.add_option(
        "--profiles", action="store_true",
        help="List the platform and configuration profiles.")
    opts, args = parser.parse_args()
    if depends is None:
        if opts.filename == "-":
            fd = sys.stdin
        elif opts.filename:
            try:
                fd = open(opts.filename, 'rt')
            except IOError:
                logging.error('Error reading file %s.' % opts.filename)
                return 1
        else:
            if (os.path.isfile('bindep.txt') and
                os.path.isfile('other-requirements.txt')):
                logging.error('Both bindep.txt and other-requirements.txt '
                              'files exist, choose one.')
                return 1
            if os.path.isfile('bindep.txt'):
                try:
                    fd = open('bindep.txt', 'rt')
                except IOError:
                    logging.error('Error reading file bindep.txt.')
                    return 1
            elif os.path.isfile('other-requirements.txt'):
                try:
                    fd = open('other-requirements.txt', 'rt')
                except IOError:
                    logging.error('Error reading file other-requirements.txt.')
                    return 1
            else:
                logging.error('Neither file bindep.txt nor file '
                              'other-requirements.txt exist.')
                return 1

        depends = bindep.depends.Depends(fd.read())
    if opts.profiles:
        logging.info("Platform profiles:")
        for profile in depends.platform_profiles():
            logging.info("%s", profile)
        logging.info("")
        logging.info("Configuration profiles:")
        for profile in depends.profiles():
            logging.info("%s", profile)
    else:
        if args:
            profiles = args
        else:
            profiles = ["default"]
        profiles = profiles + depends.platform_profiles()
        rules = depends.active_rules(profiles)
        errors = depends.check_rules(rules)
        for error in errors:
            if error[0] == 'missing':
                if opts.brief:
                    logging.info("%s", "\n".join(error[1]))
                else:
                    logging.info("Missing packages:")
                    logging.info("    %s", " ".join(error[1]))
            if error[0] == 'badversion':
                if not opts.brief:
                    logging.info("Bad versions of installed packages:")
                    for pkg, constraint, version in error[1]:
                        logging.info(
                            "    %s version %s does not match %s",
                            pkg, version, constraint)
                else:
                    for pkg, constraint, version in error[1]:
                        logging.info(
                            # add quotes because we need to pass the result
                            # with space chars
                            "'%s'",
                            # we split constraint to insert a space between the
                            # operator and the version number (required by
                            # package managers like yum)
                            ' '.join([pkg] +_split_constraint(constraint)))
        if errors:
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

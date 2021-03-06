# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os
import subprocess
import sys

import setuptools.sandbox
import twine.cli


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
setup_file = os.path.join(base_dir, 'setup.py')


def run():
    """
    Creates a sdist .tar.gz and a bdist_wheel --univeral .whl and uploads
    them to pypi

    :return:
        A bool - if the packaging and upload process was successful
    """

    git_wc_proc = subprocess.Popen(
        ['git', 'status', '--porcelain', '-uno'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=base_dir
    )
    git_wc_status, _ = git_wc_proc.communicate()

    if len(git_wc_status) > 0:
        print(git_wc_status.decode('utf-8').rstrip(), file=sys.stderr)
        print('Unable to perform release since working copy is not clean', file=sys.stderr)
        return False

    git_tag_proc = subprocess.Popen(
        ['git', 'tag', '-l', '--contains', 'HEAD'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=base_dir
    )
    tag, tag_error = git_tag_proc.communicate()

    if len(tag_error) > 0:
        print(tag_error.decode('utf-8').rstrip(), file=sys.stderr)
        print('Error looking for current git tag', file=sys.stderr)
        return False

    if len(tag) == 0:
        print('No git tag found on HEAD', file=sys.stderr)
        return False

    tag = tag.decode('ascii')

    setuptools.sandbox.run_setup(
        setup_file,
        ['sdist', 'bdist_wheel', '--universal']
    )
    twine.cli.dispatch(['upload', 'dist/oscrypto-%s*' % tag])

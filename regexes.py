#!/usr/bin/python
import re

authorSearch = re.compile('^[\D]*\D')
pubDateSearch = re.compile('(\d{4}\D?)(?=\.)')
titleSearch = re.compile('(?<=\d{4}..)(.*(\."|\. ))')

journalSearch = re.compile('(?<="\s)(.*:)')
volumeSearch = re.compile('(?<=\D)(\d*)(?=(\(|:))')
issueSearch = re.compile('(?<=\()(\d*)(?=\))')
journalPagesSearch = re.compile('(?::\s*)(\d*-\d*)')

containingVolumeInfoSearch = re.compile('(?<=( In ))(.*\d*\.)')
containingVolumeSearch = re.compile('(.*)(?=, \d*-\d*\.)')

publishingInfoSearch = re.compile('(?<=\d{4}..)(.*)')
publishingInfoExtract = re.compile('(?<=\. )(.*)(?=\.)')

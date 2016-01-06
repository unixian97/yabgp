# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

""" Unittest for MPReach NLRI"""

import unittest

from yabgp.message.attribute.mpreachnlri import MpReachNLRI


class TestMpReachNLRI(unittest.TestCase):

    def setUp(self):

        self.maxDiff = None

    def test_ipv6_unicast(self):

        data_bin = b"\x00\x02\x01\x10\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x01\x00\x80\x20\x01\x32\x32\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01" \
                   b"\x40\x20\x01\x32\x32\x00\x01\x00\x00\x7f\x20\x01\x48\x37\x16\x32\x00\x00\x00" \
                   b"\x00\x00\x00\x00\x00\x00\x02"
        data_hoped = {
            'afi_safi': (2, 1),
            'nexthop': '2001:3232::1',
            'nlri': ['2001:3232::1/128', '::2001:3232:1:0/64', '2001:4837:1632::2/127']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin))

    def test_ipv6_unicast_with_linklocal_nexthop(self):
        data_bin = b"\x00\x02\x01\x20\x20\x01\x0d\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                   b"\x02\xfe\x80\x00\x00\x00\x00\x00\x00\xc0\x02\x0b\xff\xfe\x7e\x00\x00\x00\x40" \
                   b"\x20\x01\x0d\xb8\x00\x02\x00\x02\x40\x20\x01\x0d\xb8\x00\x02\x00\x01\x40\x20" \
                   b"\x01\x0d\xb8\x00\x02\x00\x00"
        data_hoped = {
            'afi_safi': (2, 1),
            'linklocal_nexthop': 'fe80::c002:bff:fe7e:0',
            'nexthop': '2001:db8::2',
            'nlri': ['::2001:db8:2:2/64', '::2001:db8:2:1/64', '::2001:db8:2:0/64']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(data_bin))

    def test_ipv6_unicast_construct(self):
        data_parsed = {
            'afi_safi': (2, 1),
            'nexthop': '2001:3232::1',
            'nlri': ['2001:3232::1/128', '::2001:3232:1:0/64', '2001:4837:1632::2/127']}
        self.assertEqual(data_parsed, MpReachNLRI.parse(MpReachNLRI.construct(data_parsed)[3:]))

    def test_ipv6_unicast_with_locallink_nexthop_construct(self):
        data_hoped = {
            'afi_safi': (2, 1),
            'linklocal_nexthop': 'fe80::c002:bff:fe7e:0',
            'nexthop': '2001:db8::2',
            'nlri': ['::2001:db8:2:2/64', '::2001:db8:2:1/64', '::2001:db8:2:0/64']}
        self.assertEqual(data_hoped, MpReachNLRI.parse(MpReachNLRI.construct(data_hoped)[3:]))

    def test_ipv4_flowspec_parse(self):
        data_bin = b'\x80\x0e\x10\x00\x01\x85\x00\x00\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        data_dict = {'afi_safi': (1, 133), 'nexthop': '', 'nlri': [{1: '192.85.2.0/24'}, {2: '192.85.1.0/24'}]}
        self.assertEqual(data_dict, MpReachNLRI.parse(data_bin[3:]))

    def test_ipv4_flowspec_construct(self):
        data_bin = b'\x80\x0e\x10\x00\x01\x85\x00\x00\x0a\x01\x18\xc0\x55\x02\x02\x18\xc0\x55\x01'
        data_dict = {'afi_safi': (1, 133), 'nexthop': '', 'nlri': [{1: '192.85.2.0/24'}, {2: '192.85.1.0/24'}]}
        self.assertEqual(data_bin, MpReachNLRI.construct(data_dict))

if __name__ == '__main__':
    unittest.main()
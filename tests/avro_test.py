# Copyright 2020 Scale Plan Yazılım A.Ş.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import unittest

from spce import CloudEvent, Avro


class AvroEncoderTests(unittest.TestCase):

    def test_encode_required(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        encoded = Avro.encode(event)
        target = b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype\x00\x14dataschema\x00\x08time\x00\x00\x02'
        self.assertEqual(target, encoded)

    def test_encode_optional(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            subject="subject1",
            dataschema="https://particlemetrics.com/schema",
            time="2020-09-28T21:33:21Z"
        )
        encoded = Avro.encode(event)
        target = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x06\x10subject1\x1edataco'
             b'ntenttype\x00\x14dataschema\x06Dhttps://particlemetrics.com/schema\x08ti'
             b'me\x06(2020-09-28T21:33:21Z\x00\x02')
        self.assertEqual(target, encoded)

    def test_encode_string_data(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=json.dumps({"spo2": 99}),
            datacontenttype="application/json"
        )
        encoded = Avro.encode(event)

        target = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x06 application/json\x14dataschema\x00\x08time\x00\x00\x0c\x18{"spo2": 99}')
        self.assertEqual(target, encoded)

    def test_encode_binary_data(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'\x01\x02\x03\x04',
            datacontenttype="application/octet-stream"
        )
        encoded = Avro.encode(event)
        target = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x060application/octet-stream\x14dataschema\x00\x08time\x00\x00\x00\x08\x01'
             b'\x02\x03\x04')
        self.assertEqual(target, encoded)

    def test_encode_extension_attribute(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            external1="foo/bar"
        )
        encoded = Avro.encode(event)
        target = \
            (b'\x12\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x00\x14dataschema\x00\x08time\x00\x12external1\x06\x0efoo/bar\x00\x02')
        self.assertEqual(target, encoded)


class AvroDecoderTests(unittest.TestCase):

    def test_decode_required(self):
        encoded_event = b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype\x00\x14dataschema\x00\x08time\x00\x00\x02'
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        event = Avro.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_optional(self):
        encoded_event = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x06\x10subject1\x1edataco'
             b'ntenttype\x00\x14dataschema\x06Dhttps://particlemetrics.com/schema\x08ti'
             b'me\x06(2020-09-28T21:33:21Z\x00\x02')
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            subject="subject1",
            dataschema="https://particlemetrics.com/schema",
            time="2020-09-28T21:33:21Z"
        )
        event = Avro.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_string_data(self):
        encoded_event = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x06 application/json\x14dataschema\x00\x08time\x00\x00\x0c\x18{"spo2": 99}')
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=json.dumps({"spo2": 99}),
            datacontenttype="application/json"
        )
        event = Avro.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_binary_data(self):
        encoded_event = \
            (b'\x10\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x060application/octet-stream\x14dataschema\x00\x08time\x00\x00\x00\x08\x01'
             b'\x02\x03\x04')
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'\x01\x02\x03\x04',
            datacontenttype="application/octet-stream"
        )
        event = Avro.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_extension_attribute(self):
        encoded_event = \
            (b'\x12\x08type\x06 OximeterMeasured\x0csource\x06\x18oximeter/123\x04id'
             b'\x06\x081000\x16specversion\x06\x061.0\x0esubject\x00\x1edatacontenttype'
             b'\x00\x14dataschema\x00\x08time\x00\x12external1\x06\x0efoo/bar\x00\x02')
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            external1="foo/bar"
        )
        event = Avro.decode(encoded_event)
        self.assertEqual(target, event)

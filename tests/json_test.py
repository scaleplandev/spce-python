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

from spce import CloudEvent, Json


class JsonEncoderTests(unittest.TestCase):

    def test_encode_required(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        encoded = Json.encode(event)
        target = '''
            {
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0"
            }
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))

    def test_encode_optional(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            subject="subject1",
            dataschema="https://particlemetrics.com/schema",
            time="2020-09-28T21:33:21Z"
        )
        encoded = Json.encode(event)
        target = '''
            {"dataschema": "https://particlemetrics.com/schema",
             "id": "1000",
             "source": "oximeter/123",
             "specversion": "1.0",
             "subject": "subject1",
             "time": "2020-09-28T21:33:21Z",
             "type": "OximeterMeasured"
            }        
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))

    def test_encode_string_data(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=json.dumps({"spo2": 99}),
            datacontenttype="application/json"
        )
        encoded = Json.encode(event)
        target = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/json",
             "data": "{\"spo2\": 99}"
            }
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))

    def test_encode_binary_data(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'\x01\x02\x03\x04',
            datacontenttype="application/octet-stream"
        )
        encoded = Json.encode(event)
        target = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/octet-stream",
             "data_base64": "AQIDBA=="
            }
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))

    def test_encode_extension_attribute(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            external1="foo/bar"
        )
        encoded = Json.encode(event)
        target = '''
            {
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0",
             "external1": "foo/bar" 
            }
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))

    def test_encode_batch_0_items(self):
        self.assertEqual("[]", Json.encode([]))

    def test_encode_batch_1_item(self):
        event_batch = [
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1000",
                datacontenttype="application/json",
                data=json.dumps({"spo2": 99}),
            )
        ]
        encoded_batch = Json.encode(event_batch)
        target = r'''
            [{
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0",
             "datacontenttype": "application/json",
             "data": "{\"spo2\": 99}"
            }]
        '''
        self.assertEqual(json.loads(target), json.loads(encoded_batch))

    def test_encode_batch_2_items(self):
        event_batch = [
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1000",
                datacontenttype="application/json",
                data=json.dumps({"spo2": 99}),
            ),
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1001",
                datacontenttype="application/json",
                data=b'\x01binarydata\x02',
            ),
        ]
        encoded_batch = Json.encode(event_batch)
        target = r'''
            [
                {
                 "type":"OximeterMeasured",
                 "source":"oximeter/123",
                 "id":"1000",
                 "specversion":"1.0",
                 "datacontenttype": "application/json",
                 "data": "{\"spo2\": 99}"
                },
                {
                 "type":"OximeterMeasured",
                 "source":"oximeter/123",
                 "id":"1001",
                 "specversion":"1.0",
                 "datacontenttype": "application/json",
                 "data_base64": "AWJpbmFyeWRhdGEC"
                }
            ]
        '''
        self.assertEqual(json.loads(target), json.loads(encoded_batch))


class JsonDecoderTests(unittest.TestCase):

    def test_decode_required(self):
        encoded_event = '''
            {
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0"
            }
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        event = Json.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_optional(self):
        encoded_event = '''
            {"dataschema": "https://particlemetrics.com/schema",
             "id": "1000",
             "source": "oximeter/123",
             "specversion": "1.0",
             "subject": "subject1",
             "time": "2020-09-28T21:33:21Z",
             "type": "OximeterMeasured"
            }        
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            subject="subject1",
            dataschema="https://particlemetrics.com/schema",
            time="2020-09-28T21:33:21Z"
        )
        event = Json.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_string_data(self):
        encoded_event = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/json",
             "data": "{\"spo2\": 99}"
            }
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=json.dumps({"spo2": 99}),
            datacontenttype="application/json"
        )
        event = Json.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_binary_data(self):
        encoded_event = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/octet-stream",
             "data_base64": "AQIDBA=="
            }
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'\x01\x02\x03\x04',
            datacontenttype="application/octet-stream"
        )
        event = Json.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_extension_attribute(self):
        encoded_event = '''
            {
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0",
             "external1": "foo/bar" 
            }
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            external1="foo/bar"
        )
        event = Json.decode(encoded_event)
        self.assertEqual(target, event)

    def test_decode_batch_0_items(self):
        self.assertEqual([], Json.decode("[]"))

    def test_decode_batch_1_item(self):
        encoded_batch = r'''
            [{
             "type":"OximeterMeasured",
             "source":"oximeter/123",
             "id":"1000",
             "specversion":"1.0",
             "datacontenttype": "application/json",
             "data": "{\"spo2\": 99}"
            }]
        '''
        target = [
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1000",
                datacontenttype="application/json",
                data=json.dumps({"spo2": 99}),
            )
        ]
        self.assertEqual(target, Json.decode(encoded_batch))

    def test_decode_batch_2_items(self):
        encoded_batch = r'''
            [
                {
                 "type":"OximeterMeasured",
                 "source":"oximeter/123",
                 "id":"1000",
                 "specversion":"1.0",
                 "datacontenttype": "application/json",
                 "data": "{\"spo2\": 99}"
                },
                {
                 "type":"OximeterMeasured",
                 "source":"oximeter/123",
                 "id":"1001",
                 "specversion":"1.0",
                 "datacontenttype": "application/json",
                 "data_base64": "AWJpbmFyeWRhdGEC"
                }
            ]
        '''
        target = [
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1000",
                datacontenttype="application/json",
                data=json.dumps({"spo2": 99}),
            ),
            CloudEvent(
                type="OximeterMeasured",
                source="oximeter/123",
                id="1001",
                datacontenttype="application/json",
                data=b'\x01binarydata\x02',
            ),
        ]
        self.assertEqual(target, Json.decode(encoded_batch))

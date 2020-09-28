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

from spce import CloudEvent, JsonEncoder, JsonDecoder


class JsonEncoderTests(unittest.TestCase):

    def test_encode_required(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        encoded = JsonEncoder.encode(event)
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
        encoded = JsonEncoder.encode(event)
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
        encoded = JsonEncoder.encode(event)
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
        encoded = JsonEncoder.encode(event)
        target = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/octet-stream",
             "data_b64": "AQIDBA=="
            }
        '''
        self.assertEqual(json.loads(target), json.loads(encoded))


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
        event = JsonDecoder.decode(encoded_event)
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
        event = JsonDecoder.decode(encoded_event)
        self.assertEqual(target, event)

    def test_encode_string_data(self):
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
        event = JsonDecoder.decode(encoded_event)
        self.assertEqual(target, event)

    def test_encode_binary_data(self):
        encoded_event = r'''
            {
             "type": "OximeterMeasured",
             "source": "oximeter/123",
             "id": "1000",
             "specversion": "1.0",
             "datacontenttype": "application/octet-stream",
             "data_b64": "AQIDBA=="
            }
        '''
        target = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'\x01\x02\x03\x04',
            datacontenttype="application/octet-stream"
        )
        event = JsonDecoder.decode(encoded_event)
        self.assertEqual(target, event)

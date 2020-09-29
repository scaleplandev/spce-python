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

import unittest

from spce import CloudEvent


class CloudEventTestCase(unittest.TestCase):

    def test_create_event(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )

        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000")

    def test_set_subject(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            subject="patient/123"
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           subject="patient/123")

    def test_set_data(self):
        # set string data
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data='{"spo2": 99}'
        )
        self.assertFalse(event._has_binary_data)
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           data='{"spo2": 99}')

        # set binary data
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            data=b'{"spo2": 99}'
        )
        self.assertTrue(event._has_binary_data)
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           data=b'{"spo2": 99}')

    def test_set_datacontenttype(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            datacontenttype="application/json"
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           datacontenttype="application/json")

    def test_set_dataschema(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            dataschema="http://particlemetrics.com/schemas/oximeter#"
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           dataschema="http://particlemetrics.com/schemas/oximeter#")

    def test_set_time(self):
        from datetime import datetime, timezone, timedelta

        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            time="2020-09-28T21:33:21Z"
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           time="2020-09-28T21:33:21Z")

        # datetime object without timezone
        dt = datetime(2020, 9, 25, 13, 32, 56)
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            time=dt
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           time="2020-09-25T13:32:56Z")

        istanbul = timezone(timedelta(0, 10800), "+03")
        # datetime object with timezone
        dt = datetime(2020, 9, 25, 13, 32, 56).astimezone(istanbul)
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            time=dt
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           time="2020-09-25T13:32:56+03:00")




    def test_set_extension_attribute(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
            external1="foo/bar"
        )
        self.compare_event(event,
                           type="OximeterMeasured",
                           source="oximeter/123",
                           id="1000",
                           external1="foo/bar")

    def test_eq_distinct_instance(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        self.assertNotEqual(None, event)

    def test_str(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        event_str = str(event)
        target = '''{'type': 'OximeterMeasured', 'source': 'oximeter/123', 'id': '1000', 'specversion': '1.0'}'''
        self.assertEqual(target, event_str)

    def test_repr(self):
        event = CloudEvent(
            type="OximeterMeasured",
            source="oximeter/123",
            id="1000",
        )
        event_str = repr(event)
        target = '''{'type': 'OximeterMeasured', 'source': 'oximeter/123', 'id': '1000', 'specversion': '1.0'}'''
        self.assertEqual(target, event_str)

    def compare_event(self, event: CloudEvent, *,
                 type: str,
                 source: str,
                 id: str,
                 specversion="1.0",
                 subject = None,
                 data = None,
                 datacontenttype = None,
                 dataschema = None,
                 time = None,
                 **attributes
                 ):
        self.assertEqual(type, event.type)
        self.assertEqual(source, event.source)
        self.assertEqual(id, event.id)
        self.assertEqual(specversion, event.specversion)
        self.assertEqual(subject, event.subject)
        self.assertEqual(data, event.data)
        self.assertEqual(datacontenttype, event.datacontenttype)
        self.assertEqual(dataschema, event.dataschema)
        self.assertEqual(time, event.time)

        for name, value in attributes.items():
            self.assertEqual(value, event.attribute(name))


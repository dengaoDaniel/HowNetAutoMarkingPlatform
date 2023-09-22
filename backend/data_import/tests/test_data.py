import uuid

from django.test import TestCase

from data_import.pipeline.data import TextData
from examples.models import Example
from projects.tests.utils import prepare_project


class TestTextData(TestCase):
    def setUp(self):
        self.dic = {
            "example_uuid": uuid.uuid4(),
            "filename": "test.txt",
            "upload_name": "test.txt",
            "text": "test",
        }
        self.project = prepare_project()

    def test_parse(self):
        data = TextData.parse(**self.dic)
        self.assertIsInstance(data, TextData)
        self.assertEqual(data.uuid, self.dic["example_uuid"])
        self.assertEqual(data.filename, self.dic["filename"])
        self.assertEqual(data.upload_name, self.dic["upload_name"])
        self.assertEqual(data.text, self.dic["text"])

    def test_parse_empty_text(self):
        self.dic["text"] = ""
        with self.assertRaises(ValueError):
            TextData.parse(**self.dic)

    def test_create(self):
        data = TextData.parse(**self.dic)
        example = data.create(self.project.item)
        self.assertIsInstance(example, Example)
        self.assertEqual(example.uuid, self.dic["example_uuid"])



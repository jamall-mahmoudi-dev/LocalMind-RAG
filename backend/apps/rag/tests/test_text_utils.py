from django.test import SimpleTestCase
from apps.rag.text_utils import chunk_text


class ChunkTextTests(SimpleTestCase):
    def test_empty_text_returns_no_chunks(self):
        self.assertEqual(chunk_text(""), [])

    def test_short_text_returns_single_chunk(self):
        chunks = chunk_text("hello world", chunk_size=800, overlap=100)
        self.assertEqual(chunks, ["hello world"])

    def test_long_text_is_split_into_multiple_chunks(self):
        text = "a" * 2000
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        self.assertGreater(len(chunks), 1)

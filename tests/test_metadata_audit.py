import unittest
from scripts.audit_soundcloud_metadata import audit

class MetadataAuditTests(unittest.TestCase):
    def test_missing_artwork_is_critical(self):
        row={"id":1,"title":"Signal","genre":"Reggae","description":"x","permalink_url":"https://example.test"}
        result=audit([row])[0]
        self.assertEqual(result["priority"],"critical")
        self.assertIn("artwork",result["missing_fields"])

    def test_complete_core_metadata(self):
        row={"id":1,"title":"Signal","artwork_url":"cover.jpg","genre":"Reggae","description":"x","tag_list":"reggae","bpm":90,"key_signature":"Am","permalink_url":"https://example.test"}
        result=audit([row])[0]
        self.assertEqual(result["priority"],"complete")
        self.assertEqual(result["completeness_score"],100)

if __name__=="__main__": unittest.main()

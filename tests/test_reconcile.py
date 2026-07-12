import unittest
from scripts.reconcile_catalogs import normalize, base_title, reconcile

class ReconcileTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Día de Muertos!"),"dia de muertos")
    def test_base_version(self):
        self.assertEqual(base_title("Signal (Live Version)"),"signal")
    def test_classification(self):
        dk=[{"release":"A","track_number":1,"title":"Día de Muertos","artist":"Iyari Gomez"},{"release":"B","track_number":1,"title":"Signal","artist":"Iyari Gomez"}]
        sc=[{"title":"Dia de Muertos","url":"","id":"","plays":0},{"title":"Signal - Live","url":"","id":"","plays":0},{"title":"Solo SoundCloud","url":"","id":"","plays":0}]
        matched,only_sc,only_dk,review=reconcile(dk,sc,{})
        self.assertEqual(len(matched),2)
        self.assertEqual(len(only_sc),1)
        self.assertEqual(len(only_dk),0)
        self.assertEqual(len(review),0)

if __name__=="__main__": unittest.main()

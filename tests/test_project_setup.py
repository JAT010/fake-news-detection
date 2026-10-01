from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProjectSetupTest(unittest.TestCase):
    def test_runtime_requirements_include_streamlit(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
        self.assertIn("streamlit", requirements)

    def test_runtime_files_exist(self):
        self.assertTrue((ROOT / "src" / "app.py").exists())
        self.assertTrue((ROOT / "src" / "xgb_model.pkl").exists())
        self.assertTrue((ROOT / "data" / "processed" / "X_test_for_app.csv").exists())
        self.assertTrue((ROOT / "data" / "processed" / "y_test_for_app.csv").exists())


if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np
import sys
import os
sys.path.append(".")

class PyTest(unittest.TestCase):
    def test_import(self):
        try:
            __import__("cppsim")
        except:
            self.fail("Import Error")
    
    def test_body(self):
        import cppsim as cs
        self.assertTrue((cs.Body3().pos == np.array([0,0,0], dtype=np.double)).all())

class CppTest(unittest.TestCase):

    def test_vec3(self):
        self.assertEqual(os.system("./build/vec3test.elf"),0)
    
    def test_body(self):
        self.assertEqual(os.system("./build/bodytest.elf"), 0)
if __name__ == "__main__":
    unittest.main()
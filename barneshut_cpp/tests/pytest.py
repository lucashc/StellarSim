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
    
    def test_reading(self):
        import cppsim as cs
        os.system("./build/bodytest.elf")
        bl = cs.BodyList3.load("test.bin")
    
    def test_saving(self):
        import cppsim as cs
        import numpy as np
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        x.save("test2.bin")
        result = cs.BodyList3.load("test2.bin")
        self.assertTrue((x[0].pos == result[0].pos).all())
        self.assertTrue((x[1].pos == result[1].pos).all())

class CppTest(unittest.TestCase):

    def test_vec3(self):
        self.assertEqual(os.system("./build/vec3test.elf"),0)
    
    def test_body(self):
        self.assertEqual(os.system("./build/bodytest.elf"), 0)
if __name__ == "__main__":
    unittest.main()
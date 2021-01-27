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
    
    def test_saving_vectorized(self):
        import cppsim as cs
        import numpy as np
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        result = cs.LeapFrogSaveC(x, n_steps=20)
        result_np = result.numpy()
        result.save("test123.bin")
        loaded = cs.Result.load("test123.bin")
        loaded_last = cs.Result.load_last("test123.bin")
        self.assertTrue((loaded_last[1].pos == x[1].pos).all())
        loaded_np = loaded.numpy(make_copy=False)
        loaded_np_copy = loaded.numpy(make_copy=True)
        self.assertTrue((result_np[19,1].pos == loaded_np[19,1].pos).all())
        self.assertTrue((result_np[19,1].pos == loaded_np_copy[19,1].pos).all())
        del loaded_np
        self.assertTrue((result_np[19,1].pos == loaded_np_copy[19,1].pos).all())
        self.assertTrue((loaded.extract_pos()[0, 0] == loaded.numpy()[0,0].pos).all())
    
    def test_accelerated_accelerations(self):
        import cppsim as cs
        import numpy as np
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        y = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        result = cs.LeapFrogSaveC(x, n_steps=20).numpy()
        cs.acceleratedAccelerationsC(y)
        self.assertTrue((result[1, 0].g == y[0].g).all())
    
    def test_save_last(self):
        import cppsim as cs
        import numpy as np
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        result = cs.LeapFrogSaveC(x, n_steps=20)
        result.save_last_step("test.bin")
        result = result.numpy()
        bl = cs.BodyList3.load("test.bin")
        self.assertTrue((bl[0].pos == result[-1,0].pos).all())

    def test_copy(self):
        import cppsim as cs
        import numpy as np
        from copy import copy
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        b1 = cs.Body3(np.array([1,2,3], dtype=np.double))
        b2 = copy(b1)
        b1.pos = np.array([1,35,3], dtype=np.double)
        del b1
        self.assertTrue((b2.pos == np.array([1,2,3], dtype=np.double)).all())
        y  = copy(x)
        x[0].pos = np.array([1,2,3], dtype=np.double)
        del x
        self.assertTrue((y[0].pos == [0,0,0]).all())

    def test_constants(self):
        import cppsim as cs
        cs.set_r_max(10)
        self.assertEqual(cs.get_r_max(), 10)
        cs.set_rcmw(20)
        self.assertEqual(cs.get_rcmw(), 20)
        self.assertEqual(cs.get_thread_count(), 4)
        cs.set_thread_count(12)
        self.assertEqual(cs.get_thread_count(), 12)

    def test_transform(self):
        import cppsim as cs
        import numpy as np
        from copy import copy
        x = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        y = cs.BodyList3(np.array([
            cs.Body3(),
            cs.Body3(np.array([1,2,3], dtype=np.double))
        ]))
        x.translate(np.array([1,1,1], dtype=np.double))
        x.add_velocity(np.array([1,1,1], dtype=np.double))
        self.assertTrue((x[0].pos == np.array([1,1,1], dtype=np.double)).all())
        self.assertTrue((x[1].pos == np.array([2,3,4], dtype=np.double)).all())
        self.assertTrue((x[0].vel == np.array([1,1,1], dtype=np.double)).all())
        b = x + y
        self.assertTrue(len(b) == len(x) + len(y))


class CppTest(unittest.TestCase):

    def test_vec3(self):
        self.assertEqual(os.system("./build/vec3test.elf"),0)
    
    def test_body(self):
        self.assertEqual(os.system("./build/bodytest.elf"), 0)
if __name__ == "__main__":
    unittest.main()
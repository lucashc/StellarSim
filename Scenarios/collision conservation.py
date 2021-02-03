import barneshut_cpp.cppsim as cs
import helper_files.stellarConstants as sc
import helper_files.PhysQuants as PQ
import numpy as np

res = cs.Result.load("Collision.binv")
PQ.quantities(res)
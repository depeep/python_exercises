from assignment3_v2 import *
import pytest


def test_checkUserResponse():
    c=MemoryTestWindow()
    assert c.checkUserResponse([1,2,3],[1,2,3]) == True
    assert c.checkUserResponse([1,2,3],[1,2,4]) == False
    # assert c.checkUserResponse([1,2,3],[1,2,3]) == False  # deze geeft een false :)







    


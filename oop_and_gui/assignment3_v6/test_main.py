# eerste probeerse om een test te schrijven voor de checkUserResponse methode, die de user response vergelijkt met de gegenereerde sequence.

import main
import pytest



def test_checkUserResponse():
    c=main.MemoryTestWindow()
    assert c.checkUserResponse([1,2,3],[1,2,3]) == True
    assert c.checkUserResponse([1,2,3],[1,2,4]) == False
    # assert c.checkUserResponse([1,2,3],[1,2,3]) == False  # deze geeft een false :)


if __name__ == "__main__":    pytest.main()
import main
import pytest
import kleurdoos
import config
import vormen


def test_checkUserResponse():
    c=main.MemoryTestWindow()
    assert c.checkUserResponse([1,2,3],[1,2,3]) == True
    assert c.checkUserResponse([1,2,3],[1,2,4]) == False
    # assert c.checkUserResponse([1,2,3],[1,2,3]) == False  # deze geeft een false :)

# def test_runObservationPhase():
#     c=main.MemoryTestWindow()
#     kleurdoos = kleurdoos.vulKleurdoos()
#     vierkanten=c.prepareObservationPhase(kleurdoos)
#     c.runObservationPhase(vierkanten, sequenceLength=3, timeVisible=1000, timeBetween=500)
#     assert len(c.getoondeReeks) == 3
#     assert all(0 <= nummer < 4 for nummer in c.getoondeReeks)  # controleer of alle nummers in de reeks tussen 0 en 3 liggen


    

if __name__ == "__main__":    pytest.main()
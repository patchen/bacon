import nose
import bacon

def sort_dict_lists(d):
    '''
    Sort the list in the dictionary
    '''
    for value in dict.values():
        value.sort()

def test_invert_actor_dict_empty():
    assert bacon.invert_actor_dict({}) == {}, "An empty actor_dict"

def test_invert_actor_dict_single():
    assert bacon.invert_actor_dict({"Actor":["movie"]}) == {"movie": ["Actor"]}\
        ,"A single actor and movie"
    
def test_invert_actor_dict_two_movies():
    assert bacon.invert_actor_dict({"Actor":["m1","m2"]}) == {"m1":["Actor"],\
        "m2":["Actor"]},"One actor, two movies"
    
def test_invert_actor_dict_two_actors():
    assert bacon.invert_actor_dict({"A":["movie"], "B":["movie"]}) == \
        {"movie":["A","B"]},"Two actors, one movie"
    
def test_invert_actor_dict_multiple_actors_and_movies():
    assert bacon.invert_actor_dict({"A":["m1","m3","m47"], "B":["m1","m2"], \
        "C":["m3","m9"], "Actor":["m224"]}) == {"m1":["A","B"], "m2":["B"], \
        "m3":["A","C"], "m9":["C"], "m47":["A"], "m224":["Actor"]}, \
        "Multiple movies and actors"

if __name__ == '__main__':
    nose.runmodule()
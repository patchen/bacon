import nose
import bacon

#no connection Bacon Number Infinity
def test_find_connection_noconnection():
    actor_dict = {'ActA': ['m7', 'm9'],'Kevin Bacon': ['m1','m2']} 
    movie_dict = {'m7': ['ActA'],'m9': ['ActA'],'m1':['Kevin Bacon'],
                  'm2':['Kevin Bacon']}
    answer = [('None', 'Kevin Bacon')]
    assert bacon.find_connection('ActA', actor_dict, movie_dict,{})\
           == [] ,'No Connection With Bacon infinity'

#Kevin bacon not in data
def test_find_connection_nobacon():
    actor_dict = {'ActA': ['m1', 'm2'],'ActB': ['m1', 'm2', 'm3'],} 
    movie_dict = {'m1': ['ActA', 'ActB', 'ActC'],'m2': ['ActA', 'ActB']}     
    assert bacon.find_connection \
            ('Kevin Bacon', actor_dict, movie_dict,{})\
           == [], 'No Bacon in data'
    
#Kevin Bacon Number to Self 
def test_find_connection_self():
    actor_dict = {'ActA': ['m1', 'm2'],'ActB': ['m1', 'm2', 'm3'],} 
    movie_dict = {'m1': ['ActA', 'ActB', 'ActC'],
                  'm2': ['ActA', 'ActB', 'Kevin Bacon']}
    answer = []
    assert bacon.find_connection\
                           ('Kevin Bacon', actor_dict, movie_dict,{})\
           == answer, 'Kevin Bacon to self is 0'
    
# Bacon number 1
def test_find_connection_one():
    actor_dict = {'ActA': ['m1', 'm2'], 'ActB': ['m1', 'm2'], 'Kevin Bacon': ['m2']}
    movie_dict = {'m1': ['ActA', 'ActB']
                  ,'m2': ['ActA', 'ActB', 'Kevin Bacon']}
    answer = [('m2', 'Kevin Bacon')]
    assert bacon.find_connection\
                           ('ActA', actor_dict, movie_dict,{})\
           == answer, 'Bacon number 1'
# Bacon number other
def test_find_connection_other():
    actor_dict = {'ActA': ['m1', 'm2'], 
                      'ActB': ['m1', 'm2', 'm3'],  
                      'ActC': ['m1'],
                      'ActD': ['m3', 'm6'],
                      'ActE': ['m6'],
                      'ActF': ['m4'],
                      'ActG': ['m4'],
                      'ActH': ['m5'],
                      'Kevin Bacon': ['m2', 'm5']}

    movie_dict =  {'m1': ['ActA', 'ActB', 'ActC'],
                       'm2': ['ActA', 'ActB', 'Kevin Bacon'],
                       'm3': ['ActB', 'ActD'],
                       'm4': ['ActF', 'ActG'],
                       'm5': ['ActH', 'Kevin Bacon'],
                       'm6': ['ActD', 'ActE']}
    answer = [("m6", "ActD"), ("m3", "ActB"), ("m2", "Kevin Bacon")]
    assert bacon.find_connection\
                           ('ActE', actor_dict, movie_dict,{})\
           == answer, 'Bacon number 3'
# Shortest connection out of all the possible one
def test_find_connection_short():
    actor_dict = {'ActA':['m1'],'ActB': ['m1','m2'],'ActC': ['m1','m5'],\
                  'ActD':['m5,m7'],'Kevin Bacon': ['m2', 'm7']}
    movie_dict =  {'m1': ['ActA','ActB','ActC'], 'm2': ['ActB','Kevin Bacon'],\
                   'm5':['ActC', 'ActD'], 'm7':['ActD', 'Kevin Bacon']}
    answer = [('m1', 'ActB'),('m2','Kevin Bacon')]
    assert bacon.find_connection\
                           ('ActA', actor_dict, movie_dict,{})\
           == answer, 'Shortest Path'
# two possible connections
def test_find_connection_short():
    actor_dict = {'ActA':['m1'],'ActB': ['m1','m2'],'ActC': ['m1','m3'],\
                  'Kevin Bacon': ['m2', 'm3']}
    movie_dict =  {'m1': ['ActA','ActB','ActC'], 'm2': ['ActB','Kevin Bacon'],\
                   'm3':['ActC', 'Kevin Bacon']}
    answer = [('m1', 'ActB'),('m2','Kevin Bacon')]
    answer2 = [('m1', 'ActC'),('m3','Kevin Bacon')]
    result = bacon.find_connection ('ActA', actor_dict, movie_dict,{})\
    assert result == answer or assert result == answer2, 'two paths'
    
if __name__ == '__main__':
    nose.runmodule()
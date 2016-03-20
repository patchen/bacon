import urllib
import media

def invert_actor_dict (actor_dict):
    '''Return a dictionary that is the inverse of the dictionary actor_dict. 
    The returned dictionary maps movies (string) to lists of actors (string)
    appearing in the movie.'''
    
    movie_dict = {}
    for actor in actor_dict:
        for movie in actor_dict [actor]:
            if movie in movie_dict:
                movie_dict [movie].append (actor)
            else:
                movie_dict [movie] = [actor]
    return movie_dict

def parse_actor_data(actor_data):
    '''Return the actor information in the open reader actor_data as a
    dictionary. The returned dictionary contains the names of actors (string) as 
    keys (in title case) and lists of movies (string) the actor has been in as
    values.'''
    
    actor_dict = {}
    line = actor_data.readline()
    while actor_data.readline().find("THE ACTORS LIST") == -1:
        pass
    for i in range (4):
        actor_data.readline()
    line = actor_data.readline()
    while line.find ("-----------------------------------------------------------------------------") == -1:
        i = line.find('\t')        
        s = line [:i]
        line = line [i + 1:].strip()
        if s.find ('(') != -1:
            s = s [:s.find('(')].strip()
        i = s.find (',')
        if i != -1:
            actor = s [i + 2:] + " " + s [:i]
        else:
            actor = s
        actor = actor.title()
        movies = []
        while line != "":
            if line.find ("  ") != -1 and (line.find ("\t") != -1 and \
                                           line.find ("  ") < line.find ("\t") \
                                           or line.find ("\t") == -1):
                movie = line [:line.find ("  ")]
            elif line.find ("\t") != -1:
                movie = line [:line.find ("\t")]
            else:
                movie = line
            if not (movie in movies):
                movies.append (movie)
            line = actor_data.readline().strip()
        if actor in actor_dict:
            actor_dict [actor].extend (movies)
        else:
            actor_dict [actor] = movies
        line = actor_data.readline()
    return actor_dict
    

def find_connection (actor_name,actor_dict,movie_dict,connections_dict):
    '''Return a list of (movie, actor) tuples (strings) that represent a
    shortest connection between actor_name (string) and Kevin Bacon that can be
    found in the dictionaries actor_dict and movie_dict.'''
    if actor_name == "Kevin Bacon":
        return []
    else:
        investigated = []
        need_to_investigate = [actor_name]
        connection = {actor_name:[]}
        while need_to_investigate != []:
            actor = need_to_investigate.pop(0)
            investigated.append(actor)
            for movie in actor_dict[actor]:
                for co_star in movie_dict[movie]:
                    if not (co_star in investigated):
                        path = []
                        path.extend(connection[actor])
                        path.append((movie,co_star))
                    if co_star == "Kevin Bacon":
                        connections_dict[actor_name] = path 
                        return path
                    if not (co_star in investigated) and \
                       not (co_star in need_to_investigate):
                        need_to_investigate.append(co_star)
                        connection [co_star] = path
        return []
                 
    
if __name__ == "__main__":
    f = open ("large_actor_data.txt")
    actor_dict = parse_actor_data (f)
    movie_dict = invert_actor_dict (actor_dict)
    x = raw_input ("Please enter an actor (or blank to exit): ").strip().title()
    largest = 0
    while x != '':
        if not (x in actor_dict):
            print x.title() + " has a Bacon Number of Infinity."
        elif x != '':
            connection = find_connection (x, actor_dict, movie_dict, {})
            if connection == [] and x.title() != "Kevin Bacon":
                print x + " has a Bacon Number of Infinity."
            else:
                print x + " has a Bacon Number of " + str (len (connection)) + '.'
                if len (connection) > largest:
                    largest = len (connection)
            actor = x
            for step in connection:
                print actor + " was in " + step[0] + " with " + step [1] +"."
                actor = step [1]
        print ""
        x = raw_input ("Please enter an actor (or blank to exit):").strip()\
                .title()
    print "Thank you for playing! The largest Bacon Number you found was " \
          + str (largest) +"."
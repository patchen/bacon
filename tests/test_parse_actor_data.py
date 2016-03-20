import nose
import bacon
import StringIO

# no data
def test_parse_data_empty():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
    d = bacon.parse_actor_data(reader)
    assert d == {}, 'empty'
    
# remove excess info on movie title
def test_parse_data_excess():
    reader = StringIO.StringIO('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				Banned by the Media (2008) (V) {Murder in a Flash (#3.4)} (archive footage)	[Himself]

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Al Gore': \
['Banned by the Media (2008) (V) {Murder in a Flash (#3.4)} (archive footage)']}\
           , 'remove excess info'
    
# movie with quotation
def test_parse_data_quotation():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				'Hick' Town (2009)	[Himself]
						"CSI: Miami" (2002) 
						
-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Al Gore': ['\'Hick\' Town (2009)', '\"CSI: Miami\" (2002)']},\
           'quotation in title'
    
# Numerals on names = same person
def test_parse_data_numeralname():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Adams, Joey (I) 		a
						
Adams, Joey (II)		b

Adams, Joey (III)		c

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Joey Adams': ['a','b','c']}, \
           'numerals on names considered one person'
    
# one actor only one movie
def test_parse_data_onemovie():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				a

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Al Gore': ['a']}, ' An Actor is in only ONE movie'
    
# one actor two movie
def test_parse_data_twomovie():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				a
						b

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Al Gore': ['a','b']}, ' An Actor is in only TWO movie'
    
# actor distinct movie list
def test_parse_data_distinct():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				a
						b
						
Langford, Jon			c

De, Robert				d

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Jon Langford': ['c'], 'Al Gore': ['a','b'], 'Robert De': \
                 ['d']}, ' actors have distinct movie lists'
    
# actor same movie list
def test_parse_data_same():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				a
						b	
						
Langford, Jon			a
						b

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Jon Langford': ['a','b'], 'Al Gore': ['a','b']}, \
           'actors have the same movie lists'
    
# actor overlaping movie list
def test_parse_data_overlap():
    reader = StringIO.StringIO ('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

CUTTING COPYRIGHT NOTICE

THE ACTORS LIST
===============

Name					Titles
----					------
Gore, Al				c
						a
						b
						
Langford, Jon			a
						b
						d

-----------------------------------------------------------------------------
SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
    d = bacon.parse_actor_data(reader)
    assert d == {'Jon Langford': ['a','b','d'], 'Al Gore': ['c','a','b']}, \
           'actors have overlapping movie lists'
    

if __name__ == '__main__':
    nose.runmodule()
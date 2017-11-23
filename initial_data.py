from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import from other py file
from database_setup import Base, User, Category, Option, Link
import json

# which database to communicate
engine = create_engine('sqlite:///researchoption.db')
Base.metadata.bind = engine
# create session maker object
DBSession = sessionmaker(bind=engine)
# session is to exceute, and commit
session = DBSession()

# creating user data
user1 = User(name='Yukino', email='yukino.kohmoto@gmail.com')
session.add(user1)
session.commit()

category_json = json.loads("""{
  "all_categories": [
    {
      "name": "Exploratory",
      "description": "It is for a project in new area that requires explorative research to find potential of the project."
    },
    {
      "name": "Fundamental",
      "description": "It is to understand users for better decision through the project process."
    },
    {
      "name": "Generative",
      "description": "It is to Generate ideas with shared insights, which gained through iterative refinement."
    },
    {
      "name": "Communicative",
      "description": "It is to draw back stories to communicate internal and external stakeholders."
    },
    {
      "name": "Evaluative",
      "description": "It is to evaluate ideas across its usage based on the fundamental research, involving users and engineers."
    },
    {
      "name": "Applicative",
      "description": "It is to share, refine and apply the product vision, involving key team members."
    }
  ]
}""")

for e in category_json['all_categories']:
    category_input = Category( name=str(e['name']),
    description=str(e['description']),
    user_id=1
    )
    session.add(category_input)
    session.commit()

option_json = json.loads("""{
  "all_options": [
    {
      "name": "User Journey",
      "description": "It is to draw touch points, by behavior of a hypothesized group of users.",
      "cat_id": 2 
    },
    {
      "name": "Persona",
      "description": "It is to understand personality of a hypothesized group of users.",
      "cat_id": 2 
    },
    {
      "name": "Empathy Map",
      "description": "It is to gain insight about users, developing empathy for other people.",
      "cat_id": 2 
    },
    {
      "name": "Mind Map",
      "description": "It is to understand touch points.",
      "cat_id": 3 
    },
    {
      "name": "Usability Test",
      "description": "It is to identify further improvement of the product.",
      "cat_id": 5
    }
  ]
}""")
for e in option_json['all_options']:
    category_input = Option( name=str(e['name']),
    description=str(e['description']),
    cat_id=e['cat_id'],
    user_id=1
    )
    session.add(category_input)
    session.commit()

link_json = json.loads("""{
  "all_links": [
    {
      "title": "Updated Empathy Map Canvas",
      "url": "https://medium.com/the-xplane-collection/updated-empathy-map-canvas-46df22df3c8a", 
      "option_id": 3 
    },
    {
      "title": "Usability Testing",
      "url": "https://www.usability.gov/how-to-and-tools/methods/usability-testing.html",
      "option_id": 5
    },
    {
      "title": "Empathy",
      "url": "https://dschool-old.stanford.edu/wp-content/themes/dschool/method-cards/empathy-map.pdf", 
      "option_id": 3
    }
  ]
}""")

for e in link_json['all_links']:
    category_input = Link( title=str(e['title']),
    url=str(e['url']),
    option_id=e['option_id'],
    )
    session.add(category_input)
    session.commit()

print 'Data has passed!'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import from other py file
from database_setup import Base, User, Category, Option, Link

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

# create category data
cat1 = Category(name="Exploratory",
                description="""It is for a project in new area that
                            requires explorative research to find
                            potential of the project.""", user_id=1)
cat2 = Category(name="Fundamental",
                description="""It is to understand users for better
                            decision through the project process.""",
                user_id=1)
cat3 = Category(name="Generative",
                description="""It is to Generate ideas with shared insights,
                            which gained through iterative refinement.""",
                user_id=1)
cat4 = Category(name="Communicative",
                description="""It is to draw back stories to communicate
                            internal and external stakeholders.""",
                user_id=1)
cat5 = Category(name="Evaluative",
                description="""It is to evaluate ideas across its usage based on
                            the fundamental research, involving users and
                            engineers.""", user_id=1)
cat6 = Category(name="Applicative",
                description="""It is to share, refine and apply the product vision,
                            involving key team members.""", user_id=1)
session.add(cat1)
session.add(cat2)
session.add(cat3)
session.add(cat4)
session.add(cat5)
session.add(cat6)
session.commit()

# create options data
option1 = Option(name='User Journey', cat_id=2,
                 description="""It is to draw touch points, by behavior of a hypothesized
                         group of users.""", user_id=1)
option2 = Option(name='Persona', cat_id=2,
                 description="""It is to understand personality of a hypothesized group of
                         users.""", user_id=1)
option3 = Option(name='Empathy Map', cat_id=2,
                 description="""It is to gain insight about users, developing empathy for
                         other people.""", user_id=1)
option4 = Option(name='Mind map', cat_id=3,
                 description="It is to understand touch points.", user_id=1)
option5 = Option(name='Usability Test', cat_id=5,
                 description="""It is to identify further improvement of the 
                             product.""", user_id=1)
session.add(option1)
session.add(option2)
session.add(option3)
session.add(option4)
session.add(option5)
session.commit()

# create link data
link1 = Link(title='Updated Empathy Map Canvas', option_id=3,
             url='https://medium.com/the-xplane-collection/updated-empathy-map-canvas-46df22df3c8a')  # NDQA
link2 = Link(title='Usability Testing', option_id=5, 
             url='https://www.usability.gov/how-to-and-tools/methods/usability-testing.html')  # NDQA
link3 = Link(title='Emppathy Map', option_id=3,
             url='https://dschool-old.stanford.edu/wp-content/themes/dschool/method-cards/empathy-map.pdf')  # NDQA
session.add(link1)
session.add(link2)
session.add(link3)
session.commit()

print 'Data has passed!'

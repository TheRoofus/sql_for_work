from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, text, select
import json
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableDict

Base = declarative_base()
meta = MetaData


class Classes(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name_classes = Column(String(10), index=True, unique=True)

    def __repr__(self):
        return "<Classes (%s)>" % (self.name_classes)


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name_subject = Column(String(30), index=True, unique=True)

    def __repr__(self):
        return "<Subject (%s)>" % (self.name_subject)


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name_teachers = Column(String(50), index=True, unique=True)
    qualification = Column(String(50), index=True)

    def __repr__(self):
        return "<Teachers (%s, %s)>" % (self.name_teachers, self.qualification)


class LearningActivities(Base):
    __tablename__ = "learningactivities"
    id = Column(Integer, primary_key=True)
    number_classes = Column(Integer, ForeignKey(Classes.id))
    name_subject = Column(Integer, ForeignKey(Subject.id))
    name_teachers = Column(Integer, ForeignKey(Teachers.id))

    def __repr__(self):
        return "<LearningActivities (%s, %s, %s)>" % (self.number_classes, self.name_subject, self.name_teachers)


engine = create_engine('postgresql+psycopg2://postgres:zxcvbnm123@localhost:5432/postgres')

session = Session(bind=engine)
Base.metadata.create_all(engine)

session.add(Classes(name_classes='101'))
session.add(Classes(name_classes='102'))
session.add(Classes(name_classes='201'))
session.add(Classes(name_classes='202'))
session.commit()

session.add(Subject(name_subject='Physic'))
session.add(Subject(name_subject='Mathe'))
session.add(Subject(name_subject='Chemical'))
session.add(Subject(name_subject='Fitness'))
session.commit()

session.add(Teachers(name_teachers='Ivanov', qualification='Best teacher'))
session.add(Teachers(name_teachers='Petrov', qualification='Legend teacher'))
session.add(Teachers(name_teachers='Sidorov', qualification='Best teacher'))
session.add(Teachers(name_teachers='Popov', qualification='Nobel'))
session.commit()

session.add(LearningActivities(number_classes='2', name_subject='3', name_teachers='1'))
session.add(LearningActivities(number_classes='3', name_subject='4', name_teachers='3'))
session.add(LearningActivities(number_classes='4', name_subject='2', name_teachers='4'))
session.add(LearningActivities(number_classes='1', name_subject='1', name_teachers='2'))
session.commit()


def dump_sqlalchemy_classes(output_connection_srting, output_schema):
    engine = create_engine(f'{output_connection_srting}{output_schema}')
    meta = MetaData()
    meta.reflect(bind=engine)
    result = {}
    for Classes in meta.sorted_tables:
        result[Classes.id, Classes.name_classes] = [dict(row) for row in engine.execute(Classes.select())]
    return json.dumps(result)

print(dump_sqlalchemy_classes)

classes = session.query(Classes.id, Classes.name_classes).order_by(Classes.id).all()
print(str(classes))

teachers = session.query(Teachers.id, Teachers.name_teachers, Teachers.qualification).order_by(Teachers.id).all()
print(str(teachers))

learnact = session.query(LearningActivities.id, LearningActivities.name_teachers,
                         LearningActivities.number_classes, LearningActivities.name_subject).order_by(LearningActivities.id).all()

for row in learnact:
    print("Учитель", row.name_teachers, "Номер класса", row.number_classes, "Предмет", row.name_subject)
session.commit()

'''
SELECT classes.name_classes AS "Номер класса", 
	   subject.name_subject AS "Предмет",
	   teachers.name_teachers AS "ФИО учителя",
	   teachers.qualification AS "Квалификация"
FROM learningactivities
JOIN classes ON learningactivities.number_classes = classes.id
JOIN subject ON learningactivities.name_subject = subject.id
JOIN teachers ON learningactivities.name_teachers = teachers.id
'''




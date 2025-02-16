from sqlmodel import Session, create_engine, select, or_, col

from .models import Hero

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_heroes():
    hero_1 = Hero(name="Deadpond2", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy2", secret_name="Pedro Parqeador")
    hero_3 = Hero(name="Rusty-Man2", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()

        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

        print("After refreshing the heroes")
        print("Hero 1:", hero_1)
        print("Hero 2:", hero_2)
        print("Hero 3:", hero_3)
    # print heroes with ids
    print("After the session closes")
    print("Hero 1:", hero_1)
    print("Hero 2:", hero_2)
    print("Hero 3:", hero_3)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        heroes = session.exec(statement)
        # for hero in heroes:
        #     print(hero)
        print(heroes.all())
        # It can be done in a single statement
        # heroes = session.exec(select(Hero)).all()


def select_where_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        results = session.exec(statement)
        for hero in results:
            print(hero)
        # ---------------- AND operations --------------------
        s1 = select(Hero).where(Hero.age > 35, Hero.age < 45)
        s2 = select(Hero).where(Hero.age > 35).where(Hero.age < 45)
        # ---------------- OR operations ---------------------
        s3 = select(Hero).where(or_(Hero.age > 35, Hero.age < 45))
        # ----------- Use col to prevent editor confusion/error ---------------
        s4 = select(Hero).where(col(Hero.age) > 35)


def get_hero():
    # first() -> return first element in iterable otherwise return None
    # one() => looks for exactly one object, if there is None or multiple, it will throw error
    # get() with id => return object if id matches, otherwise return None
    with Session(engine) as session:
        obj = session.exec(select(Hero).where(col(Hero.id) == 1)).first()
        print(obj)
        obj2 = session.exec(select(Hero).where(Hero.id == 2)).one()
        print(obj2)
        obj3 = session.get(Hero, 3)
        print(obj3)


def get_limit_offset():
    with Session(engine) as session:
        # skip 3 objects (offset) and get 4 objects afterwards
        results = session.exec(select(Hero).offset(3).limit(4)).all()
        print(results)


def update_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.first()
        if not hero_1:
            return

        print(hero_1)

        hero_1.age = 18
        session.add(hero_1)
        session.commit()
        session.refresh(hero_1)

        print(hero_1)

def delete_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.first()
        if not hero_1:
            return

        session.delete(hero_1)
        session.commit()

        print(hero_1)

        result = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).first()
        if not result:
            print("Hero Object Got Deleted Successfully!")


def create_db_and_models():
    # SQLModel.metadata.create_all(engine)
    # create_heroes()
    # select_heroes()
    # select_where_heroes()
    # get_hero()
    # get_limit_offset()
    update_hero()
    delete_hero()


if __name__ == "__main__":
    create_db_and_models()

"""
Run this file like this =>  python -m sql_model.main
"""

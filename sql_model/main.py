from sqlmodel import Session, create_engine, SQLModel, select, or_, col

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

def create_db_and_models():
    # SQLModel.metadata.create_all(engine)
    # create_heroes()
    # select_heroes()
    select_where_heroes()


if __name__ == "__main__":
    create_db_and_models()

"""
Run this file like this =>  python -m sql_model.main
"""

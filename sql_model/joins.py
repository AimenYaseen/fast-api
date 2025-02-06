from sqlmodel import SQLModel, Field, create_engine, Session, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None)

    team_id: int | None = Field(default=None, foreign_key="team.id")


sqlite_file_name = "database2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def select_heroes():
    with Session(engine) as session:
        # statement = select(Hero, Team).where(Hero.team_id == Team.id)
        # statement = select(Hero, Team).join(Team, isouter=True)  # outer join
        statement = select(Hero, Team).join(Team)  # inner join
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)

        statement = select(Hero).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        print(results)
        for hero in results:
            print("Hero:", hero)


def main():
    # create_db_and_tables()
    # create_heroes()
    select_heroes()


if __name__ == "__main__":
    main()

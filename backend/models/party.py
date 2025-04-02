from sqlmodel import SQLModel, Field, Relationship


class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="parties")
    affiliations: list["Affiliation"] = Relationship(back_populates="party")

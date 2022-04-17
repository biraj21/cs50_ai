import termcolor
from logic import *

mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
suspects = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = suspects + rooms + weapons


def check_knowledge(knowledge):
    for sym in symbols:
        # check if this card is surely 'there' inside the envelope
        if model_check(knowledge, sym):
            termcolor.cprint(f"{sym}: YES", "green")

        # check if this card is surely 'not there' inside the envelope
        elif model_check(knowledge, Not(sym)):
            termcolor.cprint(f"{sym}: NO", "red")

        # otherwise we are not sure whether it is there inside the envelope or not
        else:
            print(f"{sym}: MAYBE")


# any of the suspects, rooms and weapons are there inside the envelope
knowledge = And(
    Or(*suspects),
    Or(*rooms),
    Or(*weapons)
)
print(knowledge)
print()

check_knowledge(knowledge)
print("-" * 50)


# my cards
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))
print(knowledge)
print()

check_knowledge(knowledge)

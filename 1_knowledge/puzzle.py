from logic import *

students = ["Gilderoy", "Minerva", "Pomona", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols = []
for student in students:
    for house in houses:
        symbols.append(Symbol(student + house))

knowledge = And()
for student in students:
    or_sym = Or()

    # every student belongs to a house (we don't which house yet)
    for house in houses:
        or_sym.add(Symbol(student + house))

        # but no student can be in more than one house
        for house2 in houses:
            if house != house2:
                knowledge.add(Implication(
                    Symbol(student + house),
                    Not(Symbol(student + house2))
                ))

    knowledge.add(or_sym)

# each student belong to different house
for house in houses:
    for s1 in students:
        for s2 in students:
            if s1 != s2:
                knowledge.add(Implication(
                    Symbol(s1 + house), Not(Symbol(s2 + house))
                ))

# Gilderoy belongs to Gryffindor or Ravenclaw
knowledge.add(Or(Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw")))

# Pomona does not belong in Slytherin.
knowledge.add(Not(Symbol("PomonaSlytherin")))

# Minerva belongs to Gryffindor
knowledge.add(Symbol("MinervaGryffindor"))

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

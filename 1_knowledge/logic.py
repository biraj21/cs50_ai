class Sentence:
    def evaluate(self, model):
        raise Exception("nothing to evaluate")

    def formula(self):
        return ""

    def symbols(self):
        return set()

    @staticmethod
    def validate(sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("sentence must be a logical sentence")

    @staticmethod
    def parenthesize(s: str):
        def is_balanced(s):
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False

                    count -= 1

            return count == 0

        # if s.isalpha() is True, then it's a Symbol so we don't parenthesize it
        if len(s) == 0 or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and is_balanced(s[1:-1])
        ):
            return s

        return f"({s})"


class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return f"¬{Sentence.parenthesize(self.operand.formula())}"

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    def __init__(self, *conjuncts):
        for conj in conjuncts:
            Sentence.validate(conj)

        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        return hash(("and", tuple(hash(conj) for conj in self.conjuncts)))

    def __repr__(self):
        conjunction = ", ".join(str(conj) for conj in self.conjuncts)
        return f"And({conjunction})"

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        return all(conj.evaluate(model) for conj in self.conjuncts)

    def formula(self):
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()

        return " ∧ ".join(
            Sentence.parenthesize(conj.formula()) for conj in self.conjuncts
        )

    def symbols(self):
        return set.union(*(conj.symbols() for conj in self.conjuncts))


class Or(Sentence):
    def __init__(self, *disjuncts):
        for disj in disjuncts:
            Sentence.validate(disj)

        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(("or", tuple(hash(disj) for disj in self.disjuncts)))

    def __repr__(self):
        disjunction = ", ".join(str(disj) for disj in self.disjuncts)
        return f"Or({disjunction})"

    def add(self, disjunct):
        Sentence.validate(disjunct)
        self.disjuncts.append(disjunct)

    def evaluate(self, model):
        return any(disj.evaluate(model) for disj in self.disjuncts)

    def formula(self):
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()

        return " ∨ ".join(
            Sentence.parenthesize(disj.formula()) for disj in self.disjuncts
        )

    def symbols(self):
        return set.union(*(disj.symbols() for disj in self.disjuncts))


class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication) and
                self.antecedent == other.antecedent and
                self.consequent == other.consequent)

    def __hash__(self):
        return hash(("implication", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({str(self.antecedent)}, {str(self.consequent)})"

    def evaluate(self, model):
        if self.antecedent.evaluate(model):
            return self.consequent.evaluate(model)

        return True

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return isinstance(other, Biconditional) and self.left == self.right

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        left_eval = self.left.evaluate(model)
        right_eval = self.right.evaluate(model)

        ltr = True  # left to right implication
        if left_eval:
            ltr = right_eval

        rtl = True  # right to left implication
        if right_eval:
            rtl = left_eval

        return ltr and rtl

    def formula(self):
        left = Sentence.parenthesize(self.left.formula())
        right = Sentence.parenthesize(self.right.formula())
        return f"{left} <=> {right}"


def model_check(knowledge, query):
    """Checks if knowledge base entails query."""

    def check_all(knowledge, query, symbols, model):
        """Checks if knowledge base entails query, given a particular model."""

        # if all symbols in the model are assigned truth values
        if len(symbols) == 0:
            if knowledge.evaluate(model):
                return query.evaluate(model)

            return True

        remaining = symbols.copy()
        sym = remaining.pop()

        model_true = model.copy()
        model_true[sym] = True

        model_false = model.copy()
        model_false[sym] = False

        return (check_all(knowledge, query, remaining, model_true) and
                check_all(knowledge, query, remaining, model_false))

    symbols = set.union(knowledge.symbols(), query.symbols())
    return check_all(knowledge, query, symbols, dict())


# my not so good implementation of model_check()
# def model_check(knowledge, query):
#     """Checks if knowledge base entails query."""

#     def create_models(symbols):
#         """Enumerates all possible models."""

#         n_models = 2 ** len(symbols)
#         models = []
#         for i in range(n_models):
#             models.append(dict())

#         n_halves = 2
#         n_same = n_models // 2
#         for sym in symbols:
#             row_index = 0
#             for i in range(n_halves // 2):
#                 for j in range(n_same):
#                     models[row_index][sym] = True
#                     row_index += 1

#                 for j in range(n_same):
#                     models[row_index][sym] = False
#                     row_index += 1

#             n_halves *= 2
#             n_same //= 2

#         return models

#     symbols = set.union(knowledge.symbols(), query.symbols())
#     models = create_models(symbols)
#     n_truths = 0
#     for model in models:
#         if knowledge.evaluate(model):
#             n_truths += 1
#             if query.evaluate(model):
#                 n_truths -= 1

#     return n_truths == 0

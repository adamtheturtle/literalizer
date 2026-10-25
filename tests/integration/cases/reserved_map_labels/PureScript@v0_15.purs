module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "if" (PInt 1)),
    (Tuple "then" (PInt 2)),
    (Tuple "else" (PInt 3)),
    (Tuple "let" (PInt 4)),
    (Tuple "in" (PInt 5)),
    (Tuple "using" (PInt 6)),
    (Tuple "missing" (PInt 7)),
    (Tuple "assert" (PInt 8)),
    (Tuple "as" (PInt 9)),
    (Tuple "Infinity" (PInt 10)),
    (Tuple "NaN" (PInt 11)),
    (Tuple "merge" (PInt 12)),
    (Tuple "Some" (PInt 13)),
    (Tuple "toMap" (PInt 14)),
    (Tuple "forall" (PInt 15)),
    (Tuple "with" (PInt 16)),
    (Tuple "ordinary" (PInt 17))
]

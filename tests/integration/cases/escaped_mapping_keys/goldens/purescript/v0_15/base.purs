module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "quote\"backslash\\" (PInt 1)),
    (Tuple "line\nbreak" (PInt 2)),
    (Tuple "$(literal)${text}" (PInt 3)),
    (Tuple "RStr prefix" (PInt 4))
]

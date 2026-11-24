module Check where


data Tuple a b = Tuple a b
data Val
    = JInt Int
    | JStr String
    | JDict (Array (Tuple String Val))


my_data :: Val
my_data = JDict [
    (Tuple "quote\"backslash\\" (JInt 1)),
    (Tuple "line\nbreak" (JInt 2)),
    (Tuple "$(literal)${text}" (JInt 3)),
    (Tuple "RStr prefix" (JInt 4))
]

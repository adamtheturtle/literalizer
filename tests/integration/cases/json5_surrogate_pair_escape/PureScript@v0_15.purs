module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "astral" (PStr "😀")),
    (Tuple "mixed" (PStr "a😀b")),
    (Tuple "count" (PInt 2)),
    (Tuple "list" (PList [PStr "😀", PInt 1])),
    (Tuple "nested" (PDict [(Tuple "inner" (PStr "😀"))]))
]

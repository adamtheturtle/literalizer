module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PInt 1)),
    (Tuple "b" (PStr "x")),
    (Tuple "e" (PList [PInt 1, PInt 2])),
    (Tuple "f" (PDict [(Tuple "g" (PStr "h"))]))
]

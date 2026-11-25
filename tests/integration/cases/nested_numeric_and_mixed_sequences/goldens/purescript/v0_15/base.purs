module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "numbers" (PList [PInt 1, PInt 2])),
    (Tuple "nested" (PDict [(Tuple "inner" (PList [PInt 3]))])),
    (Tuple "mixed" (PList [PInt 4, PStr "five"]))
]

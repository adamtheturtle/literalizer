module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "alpha" (PList [PInt 2, PList []])),
    (Tuple "beta" (PList [PInt 5, PList [PStr "x"]]))
]

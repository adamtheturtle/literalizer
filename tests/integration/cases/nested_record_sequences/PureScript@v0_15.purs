module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PDict [(Tuple "a" (PInt 1))]],
    PList [PDict [(Tuple "a" (PInt 2))]]
]

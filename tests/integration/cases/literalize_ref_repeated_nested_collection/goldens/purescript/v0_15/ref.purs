module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


shared :: Val
shared = PList [
    PList [PInt 1, PInt 2],
    PDict [(Tuple "value" (PInt 1))]
]
my_data :: Val
my_data = PList [
    shared,
    shared
]

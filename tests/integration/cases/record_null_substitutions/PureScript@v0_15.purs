module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "missing" (PInt (-1))), (Tuple "present" (PInt 1))],
    PDict [(Tuple "missing" (PInt 2)), (Tuple "present" (PInt 3))]
    ]

module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "minimum" (PInt ((-2147483647 - 1)))),
    (Tuple "neighbor" (PInt (-2147483647))),
    (Tuple "maximum" (PInt 2147483647)),
    (Tuple "nested" (PList [PInt ((-2147483647 - 1))]))
]

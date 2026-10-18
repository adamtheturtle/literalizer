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
    (Tuple "minimum" (PInt ((-0x7fffffff - 0x1)))),
    (Tuple "neighbor" (PInt (-0x7fffffff))),
    (Tuple "maximum" (PInt 0x7fffffff)),
    (Tuple "nested" (PList [PInt ((-0x7fffffff - 0x1))]))
]

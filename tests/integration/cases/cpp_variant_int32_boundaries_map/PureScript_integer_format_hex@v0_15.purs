module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "below" (PLong (-2147483649.0))),
    (Tuple "minimum" (PInt ((-0x7fffffff - 0x1)))),
    (Tuple "above" (PInt (-0x7fffffff))),
    (Tuple "nested" (PList [PInt 0x0]))
]

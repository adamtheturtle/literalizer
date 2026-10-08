module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "minimum" (PInt (-0x80000000))),
    (Tuple "below" (PLong (-3000000000.0)))
]

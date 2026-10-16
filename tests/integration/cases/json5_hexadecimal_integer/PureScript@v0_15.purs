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
    (Tuple "lower" (PLong 3735928559.0)),
    (Tuple "upper" (PInt 31)),
    (Tuple "negative" (PInt (-16))),
    (Tuple "zero" (PInt 0))
]

module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PFloat Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "value" (PFloat (-0.0)))
]

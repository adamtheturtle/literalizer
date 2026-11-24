module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PFloat Number
    | PStr String
    | PDict (Array (Tuple String Val))


std :: Val
std = PDict [
    (Tuple "nan" (PFloat (0.0 / 0.0))),
    (Tuple "positive" (PFloat (1.0 / 0.0))),
    (Tuple "negative" (PFloat (-(1.0 / 0.0))))
]

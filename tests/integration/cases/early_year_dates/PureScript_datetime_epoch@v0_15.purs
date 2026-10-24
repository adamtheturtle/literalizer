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
    (Tuple "date" (PStr "0099-05-27")),
    (Tuple "naive" (PLong (-62135551800.0))),
    (Tuple "recent" (PInt 1716804000))
]

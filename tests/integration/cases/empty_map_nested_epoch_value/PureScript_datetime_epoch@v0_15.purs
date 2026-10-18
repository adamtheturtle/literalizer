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
my_data = PList [
    PDict [(Tuple "nested" (PDict [(Tuple "times" (PList [PLong (-2208988800.0)]))]))],
    PDict []
]

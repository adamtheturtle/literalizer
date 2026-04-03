module Check where


import Data.Tuple (Tuple(..))
data Val
    = PNull
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" PStr "Alice"),
    (Tuple "score" PNull),
    (Tuple "age" PInt 30)
    ]

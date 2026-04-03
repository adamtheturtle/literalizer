module Check where


import Data.Tuple (Tuple(..))
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" PStr "Alice"),
    (Tuple "age" PInt 30),
    (Tuple "active" PBool true),
    (Tuple "score" PNull)
    ]

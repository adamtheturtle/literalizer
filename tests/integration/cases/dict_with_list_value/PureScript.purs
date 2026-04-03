module Check where


import Data.Tuple (Tuple(..))
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" PStr "Alice"),
    (Tuple "scores" PList [PInt 10, PInt 20, PInt 30])
    ]

module Check where


import Data.Tuple (Tuple(..))
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" PDict [(Tuple "x" PInt 1)]),
    (Tuple "b" PInt 2)
    ]

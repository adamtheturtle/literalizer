module Check where


import Data.Tuple (Tuple(..))
data Val
    = PInt Int
    | PFloat Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" PInt 1),
    (Tuple "b" PFloat 2.5),
    (Tuple "c" PInt 3)
    ]

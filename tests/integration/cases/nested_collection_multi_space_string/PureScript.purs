module Check where


import Data.Tuple (Tuple(..))
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "key" PStr "hello   world"), (Tuple "value" PInt 1)]
    ]

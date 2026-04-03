module Check where


import Data.Tuple (Tuple(..))
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "name" PStr "Alice"), (Tuple "age" PInt 30)],
    PDict [(Tuple "name" PStr "Bob"), (Tuple "age" PInt 25)]
    ]

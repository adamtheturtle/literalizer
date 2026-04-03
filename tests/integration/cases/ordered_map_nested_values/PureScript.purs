module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" PStr "Alice"),
    (Tuple "scores" PDict [(Tuple "1" PStr "first"), (Tuple "2" PStr "second")])
    ]

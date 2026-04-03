module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "1" PStr "one"),
    (Tuple "2" PStr "two"),
    (Tuple "42" PStr "answer")
    ]

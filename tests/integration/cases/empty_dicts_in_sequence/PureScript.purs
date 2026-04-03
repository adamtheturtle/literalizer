module Check where


import Data.Tuple (Tuple(..))
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [],
    PDict []
    ]

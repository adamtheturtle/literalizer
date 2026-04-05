module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "SGVsbG8="
    ]

module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a_b", EInt 1),
    ("a-b", EInt 2),
    ("averyveryverylongkeynamethatgoesonandonandon", EInt 3),
    ("averyveryverylongkeynamethatgoesonandmore", EInt 4)
    ]

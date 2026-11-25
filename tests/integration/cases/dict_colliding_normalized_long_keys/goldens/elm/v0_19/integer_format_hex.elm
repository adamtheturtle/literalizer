module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a_b", EInt 0x1),
    ("a-b", EInt 0x2),
    ("averyveryverylongkeynamethatgoesonandonandon", EInt 0x3),
    ("averyveryverylongkeynamethatgoesonandmore", EInt 0x4)
    ]

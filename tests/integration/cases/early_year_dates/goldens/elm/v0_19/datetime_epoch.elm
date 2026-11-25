module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("date", EStr "0099-05-27"),
    ("naive", EInt (-62135551800)),
    ("recent", EInt 1716804000)
    ]

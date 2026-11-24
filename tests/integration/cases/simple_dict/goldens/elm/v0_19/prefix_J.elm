module Check exposing (..)


type Val
    = JNull
    | JBool Bool
    | JInt Int
    | JStr String
    | JDict (List ( String, Val ))


my_data : Val
my_data = JDict [
    ("name", JStr "Alice"),
    ("age", JInt 30),
    ("active", JBool True),
    ("score", JNull)
    ]

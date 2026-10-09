module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    {- "{ -" and '{ -' stay readable -}
    {- balanced { - nested - } and trailing - } stay readable -}
    ("x", EInt 1)
    ]

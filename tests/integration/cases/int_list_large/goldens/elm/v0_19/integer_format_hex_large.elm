module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 0xf4240,
    EInt (-0x4d2),
    EInt 0xff,
    EInt (-0xa)
    ]

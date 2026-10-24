module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt (-0x2a),
    EInt 0x0,
    EInt 0x2a,
    EFloat (-1.25),
    EFloat 0.0,
    EFloat 1.25
    ]

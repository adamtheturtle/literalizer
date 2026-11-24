module Check exposing (..)


type Val
    = EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


std : Val
std = EDict [
    ("nan", EFloat (0 / 0)),
    ("positive", EFloat (1 / 0)),
    ("negative", EFloat (-(1 / 0)))
    ]

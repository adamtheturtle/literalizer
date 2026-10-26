module Check exposing (..)


type Val
    = ENull
    | EList (List Val)


value : Val
value = ENull
my_data : Val
my_data = EList [
    value,
    value,
    ENull
    ]

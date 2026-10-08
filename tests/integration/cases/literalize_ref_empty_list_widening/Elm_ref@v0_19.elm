module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


emptyValues : Val
emptyValues = EList []
integerValues : Val
integerValues = EList [
    EInt 1
    ]
my_data : Val
my_data = EList [
    emptyValues,
    integerValues
    ]

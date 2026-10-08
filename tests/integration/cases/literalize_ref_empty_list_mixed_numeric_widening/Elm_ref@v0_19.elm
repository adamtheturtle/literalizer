module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


emptyValues : Val
emptyValues = EList []
integerValues : Val
integerValues = EList [
    EInt 1
    ]
floatValues : Val
floatValues = EList [
    EFloat 1.5
    ]
my_data : Val
my_data = EList [
    emptyValues,
    integerValues,
    floatValues
    ]

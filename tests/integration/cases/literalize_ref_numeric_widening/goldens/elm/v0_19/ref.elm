module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


floatingValue : Val
floatingValue = EFloat 1.5
integerValue : Val
integerValue = EFloat 2.0
my_data : Val
my_data = EList [
    floatingValue,
    integerValue
    ]

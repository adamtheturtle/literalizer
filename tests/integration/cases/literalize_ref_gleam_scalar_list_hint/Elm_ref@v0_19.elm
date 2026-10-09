module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


refData : Val
refData = EInt 1
my_data : Val
my_data = refData

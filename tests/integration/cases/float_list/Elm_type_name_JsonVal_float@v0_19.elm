module Check exposing (..)


type JsonVal
    = EFloat Float
    | EList (List JsonVal)


my_data : JsonVal
my_data = EList [
    EFloat 1.1,
    EFloat (-2.2),
    EFloat 3.3
    ]

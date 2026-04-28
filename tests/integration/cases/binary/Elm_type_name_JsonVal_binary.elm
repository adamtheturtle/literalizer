module Check exposing (..)


type JsonVal
    = EStr String
    | EList (List JsonVal)


my_data : JsonVal
my_data = EList [
    EStr "48656c6c6f"
    ]

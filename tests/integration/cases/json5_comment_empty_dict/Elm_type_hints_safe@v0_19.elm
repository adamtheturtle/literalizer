module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


-- empty heading
-- empty body
-- after empty
my_data : Val
my_data = EDict []

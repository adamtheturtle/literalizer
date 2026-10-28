module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("user_name", EInt 1),
    ("user.name", EInt 2),
    ("user-name", EInt 3),
    ("field_name_that_is_really_quite_long_one", EInt 4),
    ("field_name_that_is_really_quite_long_two", EInt 5)
    ]

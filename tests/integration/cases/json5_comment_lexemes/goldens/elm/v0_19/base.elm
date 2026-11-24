module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- heading
    ("a", EStr "single ' // data"),
    ("b", EStr "linecontinuation"),
    ("c", EStr "\\"),  -- actual comment
    ("d", EStr "  ")  -- final comment
    ]

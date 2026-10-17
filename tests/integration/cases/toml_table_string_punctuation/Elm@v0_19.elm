module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("comma_hash", EStr "a,#b"),
    ("comma_space_hash", EStr "trail, # comment"),
    ("escaped_quote", EStr "quote \" and , #"),
    ("next_line", EStr "xy"),
    ("line_separator", EStr "x y"),
    ("paragraph_separator", EStr "x y")
    ]

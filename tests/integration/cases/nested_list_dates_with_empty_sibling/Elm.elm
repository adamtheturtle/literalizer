module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EStr "2026-01-01", EStr "2026-01-02"],
    EList [],
    EList [EStr "2026-02-03", EStr "2026-02-04"]
    ]

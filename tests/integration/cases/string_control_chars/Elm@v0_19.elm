module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "line1\r\nline2",
    EStr "line1\rline2",
    EStr "\u{0001}"
    ]

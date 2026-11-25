module Check exposing (..)


type Val
    = EStr String


my_data : Val
my_data = EStr "a\u{0007}face"

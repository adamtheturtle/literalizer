module Check exposing (..)


type Val
    = EStr String


my_data : Val
my_data = EStr "\u{0000}x"

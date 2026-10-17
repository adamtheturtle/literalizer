module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
shared :: Val
shared = PList [
    PInt 1,
    PInt 2
]


main :: Unit
main =
    let
        _ = my_data :: Val
        _ = my_data = shared
    in
    unit

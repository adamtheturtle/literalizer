module Check where


import Prelude
consume :: Val -> Unit
consume _ = unit
data Val
    = PInt Int
    | PLong Number
    | PList (Array Val)


main :: Unit
main =
    let
        _ = consume (PLong (-2147483649.0))
        _ = consume (PLong 2147483648.0)
    in
    unit

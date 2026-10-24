module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
capture :: Val -> Unit
capture _ = unit


main :: Unit
main =
    let
        _ = capture (PInt 1)
    in
    unit

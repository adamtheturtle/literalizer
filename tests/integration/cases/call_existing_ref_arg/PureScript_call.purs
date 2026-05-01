module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
send :: Val -> Unit
send _ = unit
existing :: Val
existing = PInt 42


main :: Unit
main =
    let
        _ = send existing
    in
    unit

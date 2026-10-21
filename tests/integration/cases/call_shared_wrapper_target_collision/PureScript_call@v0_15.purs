module Check where


import Prelude
check :: Val -> Unit
check _ = unit
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = check (PInt 42)
    in
    unit

module Check where


import Prelude
check_wrapper :: Val -> Unit
check_wrapper _ = unit
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = check_wrapper (PInt 42)
    in
    unit

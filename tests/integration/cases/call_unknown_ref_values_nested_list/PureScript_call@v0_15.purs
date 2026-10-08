module Check where


import Prelude
data Val
    = PList (Array Val)
process :: Val -> Unit
process _ = unit
unknown_value :: Val
unknown_value = PList []


main :: Unit
main =
    let
        _ = process (PList [unknown_value])
    in
    unit

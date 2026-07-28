module Check where


import Prelude
data Val
    = PBool Boolean
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit
known_value :: Val
known_value = PBool true
unknown_value :: Val
unknown_value = PBool true


main :: Unit
main =
    let
        _ = process known_value (PList [unknown_value])
    in
    unit

module Check where


import Prelude
data Val
    = PList (Array Val)
process :: Val -> Unit
process _ = unit
untypedValue :: Val
untypedValue = PList []


main :: Unit
main =
    let
        _ = process (PList [untypedValue, untypedValue])
    in
    unit

module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PStr "hello")
        _ = process (PInt 42)
        _ = process (PBool true)
        _ = process (PNull)
    in
    unit

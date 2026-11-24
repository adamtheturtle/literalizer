module Check where


import Prelude
process :: Val -> Val -> Unit
process _ _ = unit
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PInt 1) (PStr "hello")
        _ = process (PStr "two") (PBool false)
        _ = process (PFloat 3.5) (PNull)
    in
    unit

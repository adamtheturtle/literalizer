module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PStr "hello")
        _ = process (PInt 42)
        _ = process (PBool true)
    in
    unit

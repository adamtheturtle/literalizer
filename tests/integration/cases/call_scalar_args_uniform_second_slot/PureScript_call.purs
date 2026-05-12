module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Val -> Unit
process _ _ = unit


main :: Unit
main =
    let
        _ = process (PStr "hello") (PStr "a")
        _ = process (PInt 42) (PStr "b")
        _ = process (PBool true) (PStr "c")
    in
    unit

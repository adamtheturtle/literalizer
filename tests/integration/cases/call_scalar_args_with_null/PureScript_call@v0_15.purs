module Check where


import Prelude
data Val
    = PNull
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PNull)
        _ = process (PStr "hello")
    in
    unit

module Check where


import Prelude
process :: Val -> Unit
process _ = unit
data Val
    = PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = process (PStr "a\"b")
    in
    unit

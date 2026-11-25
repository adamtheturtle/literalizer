module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
my_str :: Val
my_str = PStr "a\"b"


main :: Unit
main =
    let
        _ = process my_str
    in
    unit

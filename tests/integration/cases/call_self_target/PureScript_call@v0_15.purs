module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
self :: Val -> Unit
self _ = unit


main :: Unit
main =
    let
        _ = self (PStr "hello")
    in
    unit

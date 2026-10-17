module Check where


import Prelude
thing :: { first_value :: Val -> Unit }
thing = { first_value: \_ -> unit }
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = thing.first_value (PInt 1)
    in
    unit

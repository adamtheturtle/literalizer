module Check where


import Prelude
obj :: { class :: Val -> Unit }
obj = { class: \_ -> unit }
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = obj.class (PInt 42)
    in
    unit

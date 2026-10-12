module Check where


import Prelude
data Val
    = PInt Int
obj :: { ZVal :: Val -> Unit }
obj = { ZVal: \_ -> unit }


main :: Unit
main =
    let
        _ = obj.ZVal (PInt 1)
    in
    unit

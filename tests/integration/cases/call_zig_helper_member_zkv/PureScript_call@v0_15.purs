module Check where


import Prelude
data Val
    = PInt Int
obj :: { ZKV :: Val -> Unit }
obj = { ZKV: \_ -> unit }


main :: Unit
main =
    let
        _ = obj.ZKV (PInt 1)
    in
    unit

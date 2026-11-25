module Check where


import Prelude
outer :: { inner :: Val -> Val -> Unit }
outer = { inner: \_ _ -> unit }
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = outer.inner (PInt 1) (PInt 2)
    in
    unit

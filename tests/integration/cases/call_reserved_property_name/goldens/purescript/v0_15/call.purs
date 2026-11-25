module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)
foo :: { class :: Val -> Unit }
foo = { class: \_ -> unit }


main :: Unit
main =
    let
        _ = foo.class (PInt 1)
    in
    unit

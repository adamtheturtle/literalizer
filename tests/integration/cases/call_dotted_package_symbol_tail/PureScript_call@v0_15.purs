module Check where


import Prelude
helper :: { list :: Val -> Unit }
helper = { list: \_ -> unit }
data Val
    = PInt Int
    | PList (Array Val)


main :: Unit
main =
    let
        _ = helper.list (PInt 1)
    in
    unit

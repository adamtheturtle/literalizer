module Check where


import Prelude
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
f :: Val -> Val -> Unit
f _ _ = unit


main :: Unit
main =
    let
        _ = f (PInt 2) (PStr "hello")  -- trailing note
        _ = f (PInt 3) (PStr "world")  -- another note
    in
    unit

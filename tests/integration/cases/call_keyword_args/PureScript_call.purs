module Check where


import Prelude
data Val
    = PFloat Number
    | PStr String
    | PList (Array Val)
throttler :: { check :: Val -> Val -> Unit }
throttler = { check: \_ _ -> unit }
emit :: forall a. a -> Unit
emit _ = unit


main :: Unit
main =
    let
        _ = emit(throttler.check (PStr "user_1") (PFloat 1000.0))
        _ = emit(throttler.check (PStr "user_2") (PFloat 2000.5))
    in
    unit

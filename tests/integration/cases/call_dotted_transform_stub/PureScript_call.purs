module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
tracer :: { emit :: forall a. a -> Unit }
tracer = { emit: \_ -> unit }


main :: Unit
main =
    let
        _ = tracer.emit(process (PStr "hello"))
        _ = tracer.emit(process (PInt 42))
        _ = tracer.emit(process (PBool true))
    in
    unit

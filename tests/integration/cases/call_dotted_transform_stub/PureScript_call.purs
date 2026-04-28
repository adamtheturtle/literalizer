module Check where


import Prelude
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit
log :: { emit :: forall a. a -> Unit }
log = { emit: \_ -> unit }


main :: Unit
main =
    let
        _ = log.emit(process (PStr "hello"))
        _ = log.emit(process (PInt 42))
        _ = log.emit(process (PBool true))
    in
    unit

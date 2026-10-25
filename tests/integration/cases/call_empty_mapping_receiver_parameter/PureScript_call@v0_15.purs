module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
api :: { process :: Val -> Unit }
api = { process: \_ -> unit }


main :: Unit
main =
    let
        _ = api.process (PDict [])
    in
    unit

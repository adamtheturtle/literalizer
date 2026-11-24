module Check where


import Prelude
api :: { worker :: { process :: Val -> Val -> Unit } }
api = { worker: { process: \_ _ -> unit } }
data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


main :: Unit
main =
    let
        _ = api.worker.process (PDict []) (PDict [])
    in
    unit

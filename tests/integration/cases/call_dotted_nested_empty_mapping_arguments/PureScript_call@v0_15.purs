module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
api :: { worker :: { process :: Val -> Val -> Unit } }
api = { worker: { process: \_ _ -> unit } }


main :: Unit
main =
    let
        _ = api.worker.process (PList [PInt 1, PDict []]) (PInt 42)
        _ = api.worker.process (PList [PInt 2, PDict [(Tuple "x" (PStr "s"))]]) (PInt 43)
    in
    unit

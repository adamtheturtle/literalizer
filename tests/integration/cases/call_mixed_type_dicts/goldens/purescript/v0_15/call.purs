module Check where


import Prelude
data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))
app :: { mgr :: { run :: Val -> Unit } }
app = { mgr: { run: \_ -> unit } }


main :: Unit
main =
    let
        _ = app.mgr.run (PDict [(Tuple "type" (PStr "create")), (Tuple "pr_id" (PStr "pr_1")), (Tuple "draft" (PBool true))])
        _ = app.mgr.run (PDict [(Tuple "type" (PStr "create")), (Tuple "pr_id" (PStr "pr_2"))])
    in
    unit

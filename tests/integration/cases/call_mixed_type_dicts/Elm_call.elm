module Check exposing (..)


type Val
    = EBool Bool
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
appMgrOp : a -> ()
appMgrOp _ = ()


main : ()
main =
    let
        _ = appMgrOp(EDict [("type", EStr "create"), ("pr_id", EStr "pr_1"), ("draft", EBool True)])
        _ = appMgrOp(EDict [("type", EStr "create"), ("pr_id", EStr "pr_2")])
    in
    ()

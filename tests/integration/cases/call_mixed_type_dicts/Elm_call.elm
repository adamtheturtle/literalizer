module Check exposing (..)


type Val
    = EBool Bool
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
appMgrOp : a -> ()
appMgrOp _ = ()


main : Program () () Never
main =
    let
        _ = appMgrOp(EDict [("type", EStr "create"), ("pr_id", EStr "pr_1"), ("draft", EBool True)])
        _ = appMgrOp(EDict [("type", EStr "create"), ("pr_id", EStr "pr_2")])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

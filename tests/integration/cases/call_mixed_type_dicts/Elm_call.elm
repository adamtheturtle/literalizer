module Check exposing (..)


type Val
    = EBool Bool
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
appMgrRun : a -> ()
appMgrRun _ = ()


main : Program () () Never
main =
    let
        _ = appMgrRun(EDict [("type", EStr "create"), ("pr_id", EStr "pr_1"), ("draft", EBool True)])
        _ = appMgrRun(EDict [("type", EStr "create"), ("pr_id", EStr "pr_2")])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

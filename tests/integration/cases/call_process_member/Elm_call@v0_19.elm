module Check exposing (..)


appProcessFetch : a -> ()
appProcessFetch _ = ()
type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


main : Program () () Never
main =
    let
        _ = appProcessFetch (EDict [("data", EStr "hello")])
        _ = appProcessFetch (EDict [("data", EInt 42)])
        _ = appProcessFetch (EDict [("data", EBool True)])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

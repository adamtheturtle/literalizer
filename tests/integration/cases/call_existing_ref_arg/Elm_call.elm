module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
send : a -> ()
send _ = ()


main : Program () () Never
main =
    let
        existing : Val
        existing = EInt 42
        _ = send(existing)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

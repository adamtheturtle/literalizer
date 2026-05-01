module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        existing : Val
        existing = EInt 42
        _ = process(existing)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

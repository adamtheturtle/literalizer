module Check exposing (..)


check : a -> ()
check _ = ()
type Val
    = EInt Int


main : Program () () Never
main =
    let
        _ = check (EInt 42)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

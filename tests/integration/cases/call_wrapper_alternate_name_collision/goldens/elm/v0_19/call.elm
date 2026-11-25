module Check exposing (..)


check_wrapper : a -> ()
check_wrapper _ = ()
type Val
    = EInt Int


main : Program () () Never
main =
    let
        _ = check_wrapper (EInt 42)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

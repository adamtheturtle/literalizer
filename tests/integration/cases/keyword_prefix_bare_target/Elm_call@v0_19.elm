module Check exposing (..)


first_value : a -> ()
first_value _ = ()
type Val
    = EInt Int


main : Program () () Never
main =
    let
        _ = first_value (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

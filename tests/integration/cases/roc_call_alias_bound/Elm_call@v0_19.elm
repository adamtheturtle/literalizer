module Check exposing (..)


process : a -> ()
process _ = ()
type Val
    = EInt Int


main : Program () () Never
main =
    let
        my_data = process (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

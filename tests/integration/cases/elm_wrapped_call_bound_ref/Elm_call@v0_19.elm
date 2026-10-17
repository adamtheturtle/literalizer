module Check exposing (..)


type Val
    = EInt Int
make_widget : a -> ()
make_widget _ = ()


main : Program () () Never
main =
    let
        value : Val
        value = EInt 1
        _ = make_widget value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

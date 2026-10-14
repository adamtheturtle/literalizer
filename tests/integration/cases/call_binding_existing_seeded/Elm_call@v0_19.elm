module Check exposing (..)


type Val
    = EInt Int
make_widget : a -> ()
make_widget _ = ()


main : Program () () Never
main =
    let
        my_data = make_widget (EInt 42)
        my_data = make_widget my_data
        _ = make_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

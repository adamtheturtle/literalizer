module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
make_widget : a -> ()
make_widget _ = ()
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        my_data = make_widget (EInt 42)
        _ = consume my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

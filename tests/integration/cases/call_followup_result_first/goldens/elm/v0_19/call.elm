module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
make_widget : a -> b -> ()
make_widget _ _ = ()
consume : a -> b -> ()
consume _ _ = ()


main : Program () () Never
main =
    let
        my_data = make_widget (EInt 42) (EInt 3)
        _ = consume my_data (EInt 3)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

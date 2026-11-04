module Check exposing (..)


make_widget : a -> ()
make_widget _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        my_data = make_widget (EList (EInt 1 :: []))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

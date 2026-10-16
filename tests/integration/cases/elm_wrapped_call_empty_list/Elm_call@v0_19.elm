module Check exposing (..)


make_widget : a -> ()
make_widget _ = ()
type Val
    = EList (List Val)


main : Program () () Never
main =
    let
        _ = make_widget (EList [])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

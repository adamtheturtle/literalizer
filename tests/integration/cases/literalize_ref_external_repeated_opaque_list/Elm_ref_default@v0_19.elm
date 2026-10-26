module Check exposing (..)


type Val
    = EList (List Val)
consume_widget : a -> ()
consume_widget _ = ()


main : Program () () Never
main =
    let
        item : Val
        item = EList []
        my_data : Val
        my_data = EList [
            item,
            item
            ]
        _ = consume_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume_widget : a -> ()
consume_widget _ = ()


main : Program () () Never
main =
    let
        shared : Val
        shared = EInt 1
        my_data : Val
        my_data = shared
        _ = consume_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

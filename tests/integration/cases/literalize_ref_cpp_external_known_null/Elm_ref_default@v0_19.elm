module Check exposing (..)


type Val
    = ENull


main : Program () () Never
main =
    let
        item : Val
        item = ENull
        my_data : Val
        my_data = ENull
        _ = (void)my_data;
        _ = my_data = item
        _ = (void)my_data;
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        item : Val
        item = EList [
            EInt 1,
            EInt 2
            ]
        my_data : Val
        my_data = EList [
            EInt 1,
            EInt 2
            ]
        _ = (void)my_data;
        _ = my_data = item
        _ = (void)my_data;
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        shared : Val
        shared = EList [
            EInt 1,
            EInt 2
            ]
        _ = my_data : Val
        _ = my_data = shared
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

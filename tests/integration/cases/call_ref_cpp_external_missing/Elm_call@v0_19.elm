module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        item : Val
        item = EList [
            EInt 1,
            EInt 2
            ]
        _ = consume item
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

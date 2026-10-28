module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        _ = consume (EList [EList [EInt 1]])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

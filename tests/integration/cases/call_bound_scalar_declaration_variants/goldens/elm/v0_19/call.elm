module Check exposing (..)


type Val
    = EInt Int
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        shared : Val
        shared = EInt 42
        _ = consume shared
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

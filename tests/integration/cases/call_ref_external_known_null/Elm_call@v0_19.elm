module Check exposing (..)


type Val
    = ENull
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        item : Val
        item = ENull
        _ = consume item
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

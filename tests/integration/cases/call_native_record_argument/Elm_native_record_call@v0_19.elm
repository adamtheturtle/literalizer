module Check exposing (..)


consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        _ = consume ({ x = 1 })
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

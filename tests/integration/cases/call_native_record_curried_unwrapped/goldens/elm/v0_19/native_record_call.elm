module Check exposing (..)


consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        _ = consume ({ name = "Ada" })
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

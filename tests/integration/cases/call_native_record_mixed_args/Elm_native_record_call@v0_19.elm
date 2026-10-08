module Check exposing (..)


consume : a -> b -> c -> ()
consume _ _ _ = ()


main : Program () () Never
main =
    let
        _ = consume ({ x = 1 }) (2) ("first")
        _ = consume ({ name = "Ada" }) (3) ("second")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

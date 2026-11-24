module Check exposing (..)


appClientConsume : a -> b -> ()
appClientConsume _ _ = ()


main : Program () () Never
main =
    let
        _ = appClientConsume ({ x = 1 }) (2)
        _ = appClientConsume ({ name = "Ada" }) (3)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


thingFirst_value : a -> ()
thingFirst_value _ = ()
type Val
    = EInt Int


main : Program () () Never
main =
    let
        _ = thingFirst_value (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

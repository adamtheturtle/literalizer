module Check exposing (..)


type Val
    = EList (List Val)
process : ()
process = ()


main : Program () () Never
main =
    let
        _ = process()
        _ = process()
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

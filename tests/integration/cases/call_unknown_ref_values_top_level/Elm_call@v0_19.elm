module Check exposing (..)


type Val
    = EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        unknown_value : Val
        unknown_value = EList []
        _ = process unknown_value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

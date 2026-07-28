module Check exposing (..)


type Val
    = EBool Bool
    | EList (List Val)
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        known_value : Val
        known_value = EBool True
        unknown_value : Val
        unknown_value = EBool True
        _ = process known_value unknown_value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

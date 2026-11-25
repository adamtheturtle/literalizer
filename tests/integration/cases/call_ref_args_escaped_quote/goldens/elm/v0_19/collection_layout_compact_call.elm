module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        my_str : Val
        my_str = EStr "a\"b"
        _ = process my_str
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

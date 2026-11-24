module Check exposing (..)


process : a -> ()
process _ = ()
type Val
    = EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EStr "a\"b")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

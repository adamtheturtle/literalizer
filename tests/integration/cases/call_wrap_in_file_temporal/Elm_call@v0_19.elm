module Check exposing (..)


check : a -> b -> ()
check _ _ = ()
type Val
    = EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = check (EStr "2024-01-15T10:30:00+00:00") (EStr "2024-06-01")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

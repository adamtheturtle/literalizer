module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
appClientFetch : a -> ()
appClientFetch _ = ()


main : Program () () Never
main =
    let
        _ = appClientFetch (EStr "hello")
        _ = appClientFetch (EStr "world")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

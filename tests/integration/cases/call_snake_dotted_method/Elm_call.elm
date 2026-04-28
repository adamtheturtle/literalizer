module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
my_appHttp_clientFetch : a -> ()
my_appHttp_clientFetch _ = ()


main : Program () () Never
main =
    let
        _ = my_appHttp_clientFetch(EStr "hello")
        _ = my_appHttp_clientFetch(EInt 42)
        _ = my_appHttp_clientFetch(EBool True)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

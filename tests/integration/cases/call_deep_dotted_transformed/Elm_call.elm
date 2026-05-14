module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
appClientFetch : a -> ()
appClientFetch _ = ()
emit : a -> ()
emit _ = ()


main : Program () () Never
main =
    let
        _ = emit (appClientFetch (EStr "hello"))
        _ = emit (appClientFetch (EInt 42))
        _ = emit (appClientFetch (EBool True))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

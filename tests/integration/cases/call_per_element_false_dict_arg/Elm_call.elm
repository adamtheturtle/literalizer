module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))
send : a -> ()
send _ = ()


main : Program () () Never
main =
    let
        _ = send(EDict [("a", EInt 1), ("b", EStr "x")])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

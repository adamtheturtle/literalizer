module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        _ = process (EList [EInt 1, EDict []]) (EInt 42)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

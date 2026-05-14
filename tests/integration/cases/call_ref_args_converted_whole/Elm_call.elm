module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        myVar : Val
        myVar = EList [
            EInt 1,
            EInt 2,
            EInt 3
            ]
        _ = process myVar
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

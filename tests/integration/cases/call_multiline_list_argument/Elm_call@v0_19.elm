module Check exposing (..)


process : a -> ()
process _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EList [
        _ =     EInt 1,
        _ =     EInt 2
        _ =     ])
        _ = process (EList [
        _ =     EInt 3
        _ =     ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process(EInt (-1))
        _ = process(EInt (-2))
        _ = process(EInt (-3))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


process : ( a, b ) -> ()
process _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process(EInt 1, EInt 2)
        _ = process(EInt 3, EInt 4)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

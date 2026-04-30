module Check exposing (..)


type Val
    = EList (List Val)
process : ()
process = ()
emit : a -> ()
emit _ = ()


main : Program () () Never
main =
    let
        _ = emit(process())
        _ = emit(process())
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

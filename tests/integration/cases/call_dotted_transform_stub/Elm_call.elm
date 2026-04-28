module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
process : a -> ()
process _ = ()
logEmit : a -> ()
logEmit _ = ()


main : Program () () Never
main =
    let
        _ = log.emit(process(EStr "hello"))
        _ = log.emit(process(EInt 42))
        _ = log.emit(process(EBool True))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

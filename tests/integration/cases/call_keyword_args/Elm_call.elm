module Check exposing (..)


type Val
    = EFloat Float
    | EStr String
    | EList (List Val)
throttlerCheck : ( a, b ) -> ()
throttlerCheck _ = ()
emit : a -> ()
emit _ = ()


main : Program () () Never
main =
    let
        _ = emit(throttlerCheck(EStr "user_1", EFloat 1000.0))
        _ = emit(throttlerCheck(EStr "user_2", EFloat 2000.5))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
objApiClientPost : a -> ()
objApiClientPost _ = ()


main : Program () () Never
main =
    let
        _ = objApiClientPost (EStr "hello")
        _ = objApiClientPost (EInt 42)
        _ = objApiClientPost (EBool True)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

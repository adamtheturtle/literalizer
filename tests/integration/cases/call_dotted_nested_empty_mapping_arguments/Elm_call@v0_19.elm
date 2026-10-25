module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
apiWorkerProcess : a -> b -> ()
apiWorkerProcess _ _ = ()


main : Program () () Never
main =
    let
        _ = apiWorkerProcess (EList [EInt 1, EDict []]) (EInt 42)
        _ = apiWorkerProcess (EList [EInt 2, EDict [("x", EStr "s")]]) (EInt 43)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

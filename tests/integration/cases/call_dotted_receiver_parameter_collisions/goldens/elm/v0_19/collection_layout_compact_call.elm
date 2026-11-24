module Check exposing (..)


apiWorkerProcess : a -> b -> ()
apiWorkerProcess _ _ = ()
type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


main : Program () () Never
main =
    let
        _ = apiWorkerProcess (EDict []) (EDict [])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

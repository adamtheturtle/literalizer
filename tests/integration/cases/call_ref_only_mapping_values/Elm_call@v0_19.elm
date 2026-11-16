module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        item : Val
        item = EInt 42
        _ = consume (EDict [("field", item)])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

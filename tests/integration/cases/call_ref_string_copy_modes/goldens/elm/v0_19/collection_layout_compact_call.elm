module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        item : Val
        item = EStr "s"
        _ = consume item
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

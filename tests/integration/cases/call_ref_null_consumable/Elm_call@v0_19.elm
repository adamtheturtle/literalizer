module Check exposing (..)


type Val
    = ENull
    | EList (List Val)
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        my_null : Val
        my_null = ENull
        regular_null : Val
        regular_null = ENull
        _ = consume my_null
        _ = consume regular_null
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

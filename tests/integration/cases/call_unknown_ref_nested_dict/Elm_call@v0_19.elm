module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        my_list : Val
        my_list = EDict [
            ("unused", EStr "value")
            ]
        _ = process (EList [EList [EDict [("inner", my_list)]]])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

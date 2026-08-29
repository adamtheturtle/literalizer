module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        big_list : Val
        big_list = EList [
            EStr "x"
            ]
        _ = process (EDict [("k", big_list)]) (EDict [("m", big_list)])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

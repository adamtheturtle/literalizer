module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
consume : a -> b -> ()
consume _ _ = ()


main : Program () () Never
main =
    let
        foo : Val
        foo = EInt 42
        _ = consume (EList [
        _ =     EDict [
        _ =         ("other", EInt 1)
        _ =         ],
        _ =     foo
        _ =     ]) (EDict [
        _ =     ("left", foo),
        _ =     ("other", EInt 1)
        _ =     ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

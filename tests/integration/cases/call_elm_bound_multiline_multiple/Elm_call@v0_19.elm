module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
f : a -> ()
f _ = ()


main : Program () () Never
main =
    let
        ref_data : Val
        ref_data = EList [
            EInt 1,
            EInt 2
            ]
        _ = f (EList [
            ref_data
            ])
        _ = f (EList [
            ref_data
            ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

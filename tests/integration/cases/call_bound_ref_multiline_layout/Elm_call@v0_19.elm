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
            EList [
                EInt 1,
                EInt 2
                ],
            EList [
                EInt 3,
                EInt 4
                ]
            ]
        _ = f (EList [
            EList [
                ref_data
                ]
            ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

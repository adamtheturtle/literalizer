module Check exposing (..)


make_widget : a -> b -> ()
make_widget _ _ = ()
type Val
    = EInt Int
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = make_widget (EList (EInt 1 :: [])) (EList (EStr "text" :: []))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

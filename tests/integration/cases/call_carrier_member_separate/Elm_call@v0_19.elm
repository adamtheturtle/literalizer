module Check exposing (..)


appGo : a -> b -> ()
appGo _ _ = ()
type Val
    = EInt Int
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = appGo (EList (EInt 1 :: [])) (EList (EStr "text" :: []))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

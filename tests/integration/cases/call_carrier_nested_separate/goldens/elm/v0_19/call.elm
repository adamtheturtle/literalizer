module Check exposing (..)


appClientGo : a -> b -> ()
appClientGo _ _ = ()
type Val
    = EInt Int
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = appClientGo (EList (EInt 1 :: [])) (EList (EStr "text" :: []))
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

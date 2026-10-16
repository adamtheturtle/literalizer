module Check exposing (..)


make_widget : a -> Json.Encode.Value
make_widget _ = Json.Encode.null
import Json.Encode


main : Program () () Never
main =
    let
        _ = make_widget (Json.Encode.list identity [])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

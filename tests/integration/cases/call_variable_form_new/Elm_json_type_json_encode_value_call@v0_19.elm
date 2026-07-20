module Check exposing (..)


make_widget : a -> Json.Encode.Value
make_widget _ = Json.Encode.null
import Json.Encode


main : Program () () Never
main =
    let
        my_data = make_widget (Json.Encode.int 42)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }

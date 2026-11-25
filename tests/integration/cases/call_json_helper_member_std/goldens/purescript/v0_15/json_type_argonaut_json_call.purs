module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
obj :: { std :: Json -> Unit }
obj = { std: \_ -> unit }


main :: Unit
main =
    let
        _ = obj.std (fromRight jsonNull (jsonParser "1"))
    in
    unit

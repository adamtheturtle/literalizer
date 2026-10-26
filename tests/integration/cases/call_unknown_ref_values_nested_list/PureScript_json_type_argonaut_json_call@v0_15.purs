module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
process :: Json -> Unit
process _ = unit
unknown_value :: Json
unknown_value = fromRight jsonNull (jsonParser "[]")


main :: Unit
main =
    let
        _ = process (fromRight jsonNull (jsonParser "[{\"$ref\": \"unknown_value\"}]"))
    in
    unit

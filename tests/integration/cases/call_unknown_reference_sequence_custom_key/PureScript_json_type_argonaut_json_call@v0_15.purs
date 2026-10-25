module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
process :: Json -> Unit
process _ = unit
untypedValue :: Json
untypedValue = fromRight jsonNull (jsonParser "[]")


main :: Unit
main =
    let
        _ = process (fromRight jsonNull (jsonParser "[{\"@reference\": \"untyped_value\"}, {\"@reference\": \"untyped_value\"}]"))
    in
    unit

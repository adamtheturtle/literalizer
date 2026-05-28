module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
process :: Json -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (fromRight jsonNull (jsonParser "\"hello\""))
        _ = process (fromRight jsonNull (jsonParser "42"))
        _ = process (fromRight jsonNull (jsonParser "true"))
    in
    unit

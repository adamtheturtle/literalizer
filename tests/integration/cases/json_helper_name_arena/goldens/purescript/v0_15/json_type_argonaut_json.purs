module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


arena :: Json
arena = fromRight jsonNull (jsonParser "{\"a\": 1}")

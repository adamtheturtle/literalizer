module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


shared :: Json
shared = fromRight jsonNull (jsonParser "null")
my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"$ref\": \"shared\"}")

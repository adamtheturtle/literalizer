module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"__proto__\": {\"x\": 1}, \"n\": {\"__proto__\": 3}, \"y\": 2}")

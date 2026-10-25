module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"within_i32\": \"2024-01-15T12:00:00Z\", \"beyond_i32\": \"2099-06-15T08:30:00Z\"}")

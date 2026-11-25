module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"date\": \"2024-01-15\", \"datetime\": \"2024-01-15T12:30:00+00:00\"}")

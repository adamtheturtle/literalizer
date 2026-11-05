module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"date\": \"0099-05-27\", \"naive\": \"0001-01-01T12:30:00Z\", \"recent\": \"2024-05-27T10:00:00Z\"}")

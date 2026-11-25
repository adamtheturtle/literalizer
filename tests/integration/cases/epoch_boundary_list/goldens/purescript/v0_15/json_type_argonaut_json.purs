module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "[\"1901-12-13T20:45:51Z\", \"1901-12-13T20:45:52Z\", \"2038-01-19T03:14:07Z\", \"2038-01-19T03:14:08Z\"]")

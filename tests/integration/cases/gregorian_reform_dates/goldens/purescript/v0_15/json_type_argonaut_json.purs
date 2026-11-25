module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"ancient_date\": \"1500-03-01\", \"modern_date\": \"2024-01-15\", \"before_date\": \"1582-10-04\", \"gap_date\": \"1582-10-10\", \"transition_date\": \"1582-10-15\", \"after_date\": \"1582-10-16\", \"before_naive\": \"1582-10-04T12:30:00.000001Z\", \"gap_naive\": \"1582-10-10T12:30:00.500000Z\", \"transition_positive\": \"1582-10-15T00:30:00+18:00\", \"transition_negative\": \"1582-10-15T23:30:00-18:00\", \"after_positive\": \"1582-10-16T00:30:00+18:00\"}")

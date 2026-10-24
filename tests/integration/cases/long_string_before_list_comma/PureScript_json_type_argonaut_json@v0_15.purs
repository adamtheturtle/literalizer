module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "[\"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.\", 1]")

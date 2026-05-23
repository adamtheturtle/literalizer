{-# LANGUAGE QuasiQuotes #-}
module Fixture_dict_with_nulls_Haskell_json_type_aeson_value_nulls where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"name": "Alice", "score": null, "age": 30} |]
main :: IO ()
main = seq my_data (return ())

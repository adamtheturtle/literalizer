{-# LANGUAGE QuasiQuotes #-}
module Fixture_dict_with_list_value_Haskell_json_type_aeson_value_existing where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"name": "Alice", "scores": [10, 20, 30]} |]
main :: IO ()
main = seq my_data (return ())

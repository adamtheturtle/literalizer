{-# LANGUAGE QuasiQuotes #-}
module Fixture_ragged_map_sequence_values_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"a": [{"item": [1]}], "b": [{"item": [2, 3]}]} |]
main :: IO ()
main = seq my_data (return ())

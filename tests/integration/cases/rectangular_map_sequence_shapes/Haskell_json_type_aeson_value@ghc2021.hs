{-# LANGUAGE QuasiQuotes #-}
module Fixture_rectangular_map_sequence_shapes_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"a": [{"item": [1]}], "b": [{"item": [2]}]} |]
main :: IO ()
main = seq my_data (return ())

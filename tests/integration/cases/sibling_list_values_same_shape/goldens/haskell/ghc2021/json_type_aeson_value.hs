{-# LANGUAGE QuasiQuotes #-}
module Fixture_sibling_list_values_same_shape_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"test": [5, ["compile", "test"]], "package": [7, ["link", "test"]]} |]
main :: IO ()
main = seq my_data (return ())

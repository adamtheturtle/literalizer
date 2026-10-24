{-# LANGUAGE QuasiQuotes #-}
module Fixture_epoch_datetime_map_values_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"within_i32": "2024-01-15T12:00:00Z", "beyond_i32": "2099-06-15T08:30:00Z"} |]
main :: IO ()
main = seq my_data (return ())

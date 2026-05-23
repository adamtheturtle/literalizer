{-# LANGUAGE QuasiQuotes #-}
module Fixture_date_set_Haskell_json_type_aeson_value_date_set where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["2024-01-15", "2024-06-01"] |]
main :: IO ()
main = seq my_data (return ())

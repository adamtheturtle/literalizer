{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_time_Haskell_json_type_aeson_value_time where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"starts_at": "09:30:00"} |]
main :: IO ()
main = seq my_data (return ())

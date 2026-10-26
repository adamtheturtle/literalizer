{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_datetime_seconds_microsecond_Haskell_json_type_aeson_value_datetime_iso where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2024-01-15T12:30:45.123456Z" |]
main :: IO ()
main = seq my_data (return ())

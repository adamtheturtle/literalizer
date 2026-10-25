{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_datetime_microsecond_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2024-01-15T12:30:00.123456+00:00" |]
main :: IO ()
main = seq my_data (return ())

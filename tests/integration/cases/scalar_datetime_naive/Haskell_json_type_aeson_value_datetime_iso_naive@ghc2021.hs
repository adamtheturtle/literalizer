{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_datetime_naive_Haskell_json_type_aeson_value_datetime_iso_naive where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2024-01-15T12:30:00Z" |]
main :: IO ()
main = seq my_data (return ())

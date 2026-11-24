{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_datetime_whole_hour_offset_Haskell_json_type_aeson_value_datetime_epoch where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2024-01-15T18:00:00+05:00" |]
main :: IO ()
main = seq my_data (return ())

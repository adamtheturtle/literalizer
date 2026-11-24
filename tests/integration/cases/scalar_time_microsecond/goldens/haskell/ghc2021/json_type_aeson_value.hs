{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_time_microsecond_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"exact_millisecond": "09:30:15.123000", "sub_millisecond": "09:30:15.123456"} |]
main :: IO ()
main = seq my_data (return ())

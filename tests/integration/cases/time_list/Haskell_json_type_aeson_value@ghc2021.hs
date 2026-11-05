{-# LANGUAGE QuasiQuotes #-}
module Fixture_time_list_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"times": ["09:30:00", "17:45:00", "23:59:59"]} |]
main :: IO ()
main = seq my_data (return ())

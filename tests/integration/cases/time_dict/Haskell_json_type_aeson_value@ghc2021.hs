{-# LANGUAGE QuasiQuotes #-}
module Fixture_time_dict_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"morning": "09:30:00", "afternoon": "14:15:00", "evening": "23:59:59"} |]
main :: IO ()
main = seq my_data (return ())

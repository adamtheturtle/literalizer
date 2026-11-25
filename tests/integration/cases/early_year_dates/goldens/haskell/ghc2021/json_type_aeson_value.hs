{-# LANGUAGE QuasiQuotes #-}
module Fixture_early_year_dates_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"date": "0099-05-27", "naive": "0001-01-01T12:30:00Z", "recent": "2024-05-27T10:00:00Z"} |]
main :: IO ()
main = seq my_data (return ())

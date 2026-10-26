{-# LANGUAGE QuasiQuotes #-}
module Fixture_empty_key_is_data_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [{"": "external_value"}] |]
main :: IO ()
main = seq my_data (return ())

{-# LANGUAGE QuasiQuotes #-}
module Fixture_json_string_escaping_Haskell_json_type_aeson_value_string_escaping where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "a\"b\tcé" |]
main :: IO ()
main = seq my_data (return ())

{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_with_percent_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["100% done", "%(name) is here"] |]
main :: IO ()
main = seq my_data (return ())

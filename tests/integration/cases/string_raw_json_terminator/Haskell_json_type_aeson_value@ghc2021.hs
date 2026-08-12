{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_raw_json_terminator_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {")json": "x"} |]
main :: IO ()
main = seq my_data (return ())

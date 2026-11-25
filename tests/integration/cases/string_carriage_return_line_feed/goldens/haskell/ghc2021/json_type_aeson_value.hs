{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_carriage_return_line_feed_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"cr": "a\rb", "crlf": "a\r\nb", "lf": "a\nb"} |]
main :: IO ()
main = seq my_data (return ())

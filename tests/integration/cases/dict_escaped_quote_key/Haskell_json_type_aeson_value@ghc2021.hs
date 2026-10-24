{-# LANGUAGE QuasiQuotes #-}
module Fixture_dict_escaped_quote_key_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"a\"b": 1} |]
main :: IO ()
main = seq my_data (return ())

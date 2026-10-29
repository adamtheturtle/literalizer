{-# LANGUAGE QuasiQuotes #-}
module Fixture_bom_in_string_value_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"v": "a﻿b"} |]
main :: IO ()
main = seq my_data (return ())

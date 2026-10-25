{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_value_type_nested_object_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
shared :: Value
shared = [aesonQQ| [1, 2] |]
build :: Value
build = [aesonQQ| [1, 2] |]
jsonObject :: Value
jsonObject = [aesonQQ| [1, 2] |]
jsonAllocator :: Value
jsonAllocator = [aesonQQ| [1, 2] |]
jsonEntries :: Value
jsonEntries = [aesonQQ| [1, 2] |]
jsonEntry :: Value
jsonEntry = [aesonQQ| [1, 2] |]
my_data :: Value
my_data = [aesonQQ| {"field": #{shared}, "nested": [#{shared}, {}], "build": #{build}, "json_object": #{jsonObject}, "json_allocator": #{jsonAllocator}, "json_entries": #{jsonEntries}, "json_entry": #{jsonEntry}} |]
main :: IO ()
main = seq my_data (return ())

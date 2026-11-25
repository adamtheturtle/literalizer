{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_value_type_root_array_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
shared :: Value
shared = [aesonQQ| [1, 2] |]
my_data :: Value
my_data = shared
main :: IO ()
main = seq my_data (return ())

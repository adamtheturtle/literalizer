{-# LANGUAGE QuasiQuotes #-}
module Fixture_four_dimensional_empty_lists_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [[[[]]], [[[]]]] |]
main :: IO ()
main = seq my_data (return ())

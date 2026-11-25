{-# LANGUAGE QuasiQuotes #-}
module Fixture_epoch_scalar_above_i32_range_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "2099-06-15T08:30:00Z" |]
main :: IO ()
main = seq my_data (return ())

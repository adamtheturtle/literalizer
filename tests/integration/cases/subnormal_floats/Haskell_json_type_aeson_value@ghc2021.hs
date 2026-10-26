{-# LANGUAGE QuasiQuotes #-}
module Fixture_subnormal_floats_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [5e-324, -5e-324, 1e-310] |]
main :: IO ()
main = seq my_data (return ())

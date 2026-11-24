{-# LANGUAGE QuasiQuotes #-}
module Fixture_json_type_scalar_comment_Haskell_json_type_aeson_value_scalar_comment where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
-- leading
my_data :: Value
my_data = [aesonQQ| 1 |]
main :: IO ()
main = seq my_data (return ())

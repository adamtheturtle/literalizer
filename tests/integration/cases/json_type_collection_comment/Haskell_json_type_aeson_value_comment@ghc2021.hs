{-# LANGUAGE QuasiQuotes #-}
module Fixture_json_type_collection_comment_Haskell_json_type_aeson_value_comment where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
-- About a.
my_data :: Value
my_data = [aesonQQ| {"a": 1, "b": 2} |]
main :: IO ()
main = seq my_data (return ())

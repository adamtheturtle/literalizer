{-# LANGUAGE QuasiQuotes #-}
module Fixture_sequence_ragged_siblings_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [["set_task", "web", "lint_web"], ["merge_pipelines"]] |]
main :: IO ()
main = seq my_data (return ())

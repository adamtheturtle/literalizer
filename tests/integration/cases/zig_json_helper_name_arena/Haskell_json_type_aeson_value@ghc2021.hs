{-# LANGUAGE QuasiQuotes #-}
module Fixture_zig_json_helper_name_arena_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
arena :: Value
arena = [aesonQQ| {"a": 1} |]
main :: IO ()
main = seq arena (return ())

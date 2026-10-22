{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_with_backslash_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["C:\\path\\to\\file", "back\\\\slash", "hello \\\"world\\\"", "path\\to \"# file", "trailing\\", "both \"quotes''' here", "line1\\nline2\nwith newline"] |]
main :: IO ()
main = seq my_data (return ())

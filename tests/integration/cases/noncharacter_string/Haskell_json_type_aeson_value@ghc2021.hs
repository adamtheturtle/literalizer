{-# LANGUAGE QuasiQuotes #-}
module Fixture_noncharacter_string_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"fffe": "￾", "ffff": "￿"} |]
main :: IO ()
main = seq my_data (return ())

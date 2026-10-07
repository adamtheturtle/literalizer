{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_compact_separators_Haskell_native_record where
data Val0 = Val0 { name :: String, active :: Bool }
my_data :: [Val0]
my_data = [
    Val0 { name = "Ada", active = True }
    ]
main :: IO ()
main = seq my_data (return ())

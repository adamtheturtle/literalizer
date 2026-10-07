{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_native_record_boolean_fields_Haskell_native_record where
data Val0 = Val0 { active :: Bool }
my_data :: [Val0]
my_data = [
    Val0 { active = True },
    Val0 { active = False }
    ]
main :: IO ()
main = seq my_data (return ())

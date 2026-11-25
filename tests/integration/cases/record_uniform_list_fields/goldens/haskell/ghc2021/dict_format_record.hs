{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_record_uniform_list_fields_Haskell_dict_format_record where
data Val0 = Val0 { scores :: [Integer] }
my_data :: [Val0]
my_data = [
    Val0 { scores = [1, 2] },
    Val0 { scores = [3, 4] }
    ]
main :: IO ()
main = seq my_data (return ())

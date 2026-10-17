{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_kotlin_list_of_maps_with_lists_Haskell_dict_format_record where
data Val0 = Val0 { a :: [Integer] }
my_data :: [Val0]
my_data = [
    Val0 { a = [1] },
    Val0 { a = [2] }
    ]
main :: IO ()
main = seq my_data (return ())

{-# LANGUAGE DuplicateRecordFields #-}
module Fixture_ragged_map_sequence_values_Haskell_dict_format_record where
data Val1 = Val1 { item :: [Integer] }
data Val0 = Val0 { a :: [Val1], b :: [Val1] }
my_data :: Val0
my_data = Val0 {
    a = [
        Val1 {
            item = [
                1
                ]
        }
        ],
    b = [
        Val1 {
            item = [
                2,
                3
                ]
        }
        ]
}
main :: IO ()
main = seq my_data (return ())

module Fixture_date_set_Haskell_date_iso where
data Val = HSet [Val] | HStr String
my_data :: Val
my_data = HSet [
    HStr "2024-01-15",
    HStr "2024-06-01"
    ]
main :: IO ()
main = seq my_data (return ())

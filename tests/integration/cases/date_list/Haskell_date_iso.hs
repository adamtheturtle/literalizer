module Fixture_date_list_Haskell_date_iso where
data Val = HList [Val] | HStr String
my_data :: Val
my_data = HList [
    HStr "2024-01-15",
    HStr "2024-02-20"
    ]

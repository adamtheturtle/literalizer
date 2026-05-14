module Fixture_empty_list_Haskell_type_hints_safe_dt_iso where
data Val = HList [Val]
my_data :: Val
my_data = HList []
main :: IO ()
main = seq my_data (return ())

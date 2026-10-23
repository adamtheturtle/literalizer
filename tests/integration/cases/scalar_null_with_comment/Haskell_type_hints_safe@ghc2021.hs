module Fixture_scalar_null_with_comment_Haskell_type_hints_safe where
data Val = HNull
my_data :: Val
my_data = HNull  -- note
main :: IO ()
main = seq my_data (return ())

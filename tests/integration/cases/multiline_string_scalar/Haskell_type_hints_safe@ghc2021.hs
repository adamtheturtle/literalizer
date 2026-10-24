module Fixture_multiline_string_scalar_Haskell_type_hints_safe where
data Val = HStr String
my_data :: Val
my_data = HStr "\nroot first line\n  indented\n\nroot last line\n"
main :: IO ()
main = seq my_data (return ())

module Fixture_scalar_string_embedded_nul_Haskell_scalar_string_embedded_nul where
data Val = HStr String
my_data :: Val
my_data = HStr "\x00x"
main :: IO ()
main = seq my_data (return ())

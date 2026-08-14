module Fixture_haskell_c1_controls_Haskell where
data Val = HStr String
my_data :: Val
my_data = HStr "\x7f\&0\x80\&a\x9f\&F"
main :: IO ()
main = seq my_data (return ())

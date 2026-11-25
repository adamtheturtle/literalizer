module Fixture_custom_root_multiline_text_Haskell where
data Val = HStr String
custom_data :: Val
custom_data = HStr "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"
main :: IO ()
main = seq custom_data (return ())

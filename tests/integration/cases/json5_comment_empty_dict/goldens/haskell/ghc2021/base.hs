module Fixture_json5_comment_empty_dict_Haskell where
data Val = HStr String | HMap [(String, Val)]
-- empty heading
-- empty body
-- after empty
my_data :: Val
my_data = HMap []
main :: IO ()
main = seq my_data (return ())

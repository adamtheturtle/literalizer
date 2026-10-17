module Fixture_yaml_anchor_marks_in_comment_Haskell where
data Val = HNull
-- An anchor and an alias marker, written only inside this comment: &a *a
my_data :: Val
my_data = HNull
main :: IO ()
main = seq my_data (return ())

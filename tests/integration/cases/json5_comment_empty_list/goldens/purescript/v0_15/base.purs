module Check where


data Val
    = PList (Array Val)


-- empty heading
-- empty body
-- after empty
my_data :: Val
my_data = PList []

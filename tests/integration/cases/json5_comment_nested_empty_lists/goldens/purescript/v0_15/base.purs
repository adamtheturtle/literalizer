module Check where


data Val
    = PList (Array Val)


my_data :: Val
my_data = PList [
    -- outer heading
    -- first empty
    PList [],
    -- second empty
    PList []
]

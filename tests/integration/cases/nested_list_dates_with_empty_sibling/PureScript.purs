module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PStr "2026-01-01", PStr "2026-01-02"],
    PList [],
    PList [PStr "2026-02-03", PStr "2026-02-04"]
    ]

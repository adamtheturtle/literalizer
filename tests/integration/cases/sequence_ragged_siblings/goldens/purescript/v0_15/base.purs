module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PStr "set_task", PStr "web", PStr "lint_web"],
    PList [PStr "merge_pipelines"]
]

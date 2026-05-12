module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [
        (Tuple "type" (PStr "create")),
        (Tuple "pr_id" (PStr "pr_1")),
        (Tuple "draft" (PBool true))
        ],
    PDict [
        (Tuple "type" (PStr "create")),
        (Tuple "pr_id" (PStr "pr_2"))
        ]
    ]

datatype val_t =
    SBool of bool
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [
        ("type", SStr "create"),
        ("pr_id", SStr "pr_1"),
        ("draft", SBool true)
    ],
    SMap [
        ("type", SStr "create"),
        ("pr_id", SStr "pr_2")
    ]
]
val _ = my_data

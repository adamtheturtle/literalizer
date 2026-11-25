datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val deep : val_t = SList [
    SList [
        SStr "one",
        SStr "two"
    ],
    SList [
        SStr "three",
        SStr "four"
    ]
]
val my_data : val_t = SMap [
    ("a", SMap [
        ("b", SMap [
            ("c", deep)
        ])
    ])
]
val _ = my_data

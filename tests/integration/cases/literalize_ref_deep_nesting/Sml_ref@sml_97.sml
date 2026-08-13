datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val deep : val_t = SList [
    SList [
        SInt 1,
        SInt 2
    ],
    SList [
        SInt 3,
        SInt 4
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

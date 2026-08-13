module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let deep : val_t = OList [
    OList [
        OInt 1;
        OInt 2
    ];
    OList [
        OInt 3;
        OInt 4
    ]
]
let my_data : val_t = OMap [
    ("a", OMap [
        ("b", OMap [
            ("c", deep)
        ])
    ])
]

end

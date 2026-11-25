module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let deep : val_t = OList [
    OList [
        OStr "one";
        OStr "two"
    ];
    OList [
        OStr "three";
        OStr "four"
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

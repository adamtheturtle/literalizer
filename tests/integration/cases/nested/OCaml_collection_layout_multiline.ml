module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("users", OList [
        OMap [
            ("name", OStr "Bob");
            ("tags", OList [
                OStr "admin";
                OStr "user"
            ])
        ];
        OMap [
            ("name", OStr "Carol");
            ("tags", OList [
                OStr "guest"
            ])
        ]
    ])
]

end

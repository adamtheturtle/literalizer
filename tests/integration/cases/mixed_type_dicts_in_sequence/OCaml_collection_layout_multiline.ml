module Check = struct

type val_t =
  | OBool of bool
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [
        ("type", OStr "create");
        ("pr_id", OStr "pr_1");
        ("draft", OBool true)
    ];
    OMap [
        ("type", OStr "create");
        ("pr_id", OStr "pr_2")
    ]
]

end

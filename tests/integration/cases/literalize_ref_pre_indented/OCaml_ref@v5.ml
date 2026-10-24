module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
    let shared : val_t = OList [
        OInt 1;
        OInt 2
    ]
    let my_data : val_t = OMap [
        ("a", shared)
    ]

end

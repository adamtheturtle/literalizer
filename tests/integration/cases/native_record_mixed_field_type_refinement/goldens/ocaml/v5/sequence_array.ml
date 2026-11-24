module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("first", OMap [("items", OArray [|OInt 1; OMap [("value", OInt 2)]|])]);
    ("second", OMap [("items", OArray [|OInt 1; OMap [("value", OStr "s")]|])])
]

end

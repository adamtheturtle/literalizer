module Check = struct

type val_t =
  | OStr of string
  | OInt of int
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("positive", OArray [|OMap [("item", OArray [|OInt 2147483648|])]|]);
    ("negative", OArray [|OMap [("item", OArray [|OInt (-2147483649)|])]|]);
    ("mixed", OArray [|OMap [("item", OArray [|OInt 0; OInt 2147483648|])]|])
]

end

module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("lint", OArray [|OInt 2; OArray [||]|]);
    ("test", OArray [|OInt 5; OArray [|OStr "compile"|]|]);
    ("package", OArray [|OInt 7; OArray [|OStr "link"; OStr "test"|]|])
]

end

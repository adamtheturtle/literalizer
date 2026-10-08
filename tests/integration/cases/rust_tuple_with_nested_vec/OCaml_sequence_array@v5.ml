module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("lint", [|OInt 2; [||]|]);
    ("test", [|OInt 5; [|OStr "compile"|]|]);
    ("package", [|OInt 7; [|OStr "link"; OStr "test"|]|])
]

end

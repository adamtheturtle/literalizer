module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let std : val_t = OMap [
    ("a", OInt 1)
]
let arena : val_t = OMap [
    ("a", OInt 1)
]
let allocator : val_t = OMap [
    ("a", OInt 1)
]
let my_data : val_t = OList [
    std;
    arena;
    allocator
]

end

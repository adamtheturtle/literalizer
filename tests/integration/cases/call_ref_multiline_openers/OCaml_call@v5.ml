module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let consume _ = ()
let foo : val_t = OInt 42
let _ = consume(OList [
    OMap [
        ("other", OInt 1)
    ];
    foo
], OMap [
    ("left", foo);
    ("other", OInt 1)
])

end

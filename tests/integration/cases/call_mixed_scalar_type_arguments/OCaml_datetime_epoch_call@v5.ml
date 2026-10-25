module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | ODate of (int * int * int)
  | OInt of int
  | OList of val_t list
let capture _ = ()
let _ = capture(OFloat nan, OFloat infinity, OFloat neg_infinity, OFloat 1.25, ODate (2024, 1, 15), OInt 1705322096, OStr "[ordinary text]")

end

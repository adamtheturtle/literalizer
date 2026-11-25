module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let capture _ = ()
let _ = capture(OFloat nan, OFloat infinity, OFloat neg_infinity, OFloat 1.25, OStr "2024-01-15", ODatetime ((2024, 1, 15), (12, 34, 56)), OStr "[ordinary text]")

end

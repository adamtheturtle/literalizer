module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.";
    OInt 1
]

end

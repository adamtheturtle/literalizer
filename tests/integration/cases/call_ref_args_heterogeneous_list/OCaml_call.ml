module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let my_ints : val_t = OList [
    OInt 1;
    OInt 2;
    OInt 3
]
let my_strings : val_t = OList [
    OStr "a";
    OStr "b"
]
let _ = process(my_ints, 42)
let _ = process(my_strings, 7)

end

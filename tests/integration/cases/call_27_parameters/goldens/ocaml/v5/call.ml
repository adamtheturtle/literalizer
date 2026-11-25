module Check = struct

let process _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = process(OInt 0, OInt 1, OInt 2, OInt 3, OInt 4, OInt 5, OInt 6, OInt 7, OInt 8, OInt 9, OInt 10, OInt 11, OInt 12, OInt 13, OInt 14, OInt 15, OInt 16, OInt 17, OInt 18, OInt 19, OInt 20, OInt 21, OInt 22, OInt 23, OInt 24, OInt 25, OInt 26)

end

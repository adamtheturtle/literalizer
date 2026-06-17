module Check = struct

let put _ = ()
let get _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = put(1, 10)
let _ = get(1)

end

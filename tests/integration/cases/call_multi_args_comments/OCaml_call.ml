module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let _ = process(1, 0, 3600)  (* Jan 1 1970 00:00:00 - 01:00:00 *)
let _ = process(5, 0, 3600)  (* Jan 1 1970 00:00:05 - 01:00:05 *)
let _ = process(2, 0, 5400)  (* Jan 1 1970 00:00:02 - 01:30:02 *)

end

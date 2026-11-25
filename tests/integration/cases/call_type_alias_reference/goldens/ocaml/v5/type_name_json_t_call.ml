module Check = struct

type json_t =
  | OInt of int
let process _ = ()
let value : json_t = OInt 1
let _ = process(value)

end

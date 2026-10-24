module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* A JSONC input case with both comment forms. *)
    ("url", OStr "https://example.org/a/*b*/");  (* detail *)
    (* continued *)
    ("count", OInt 0x2)  (* trailing line comment *)
]

end

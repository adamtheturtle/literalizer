module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    (* strings stay data *)
    OStr "https://example.org/a/*b*/";  (* URL annotation *)
    OStr "escaped quote: \" // still data";
    OStr "backslash: \\";  (* outside the string *)
    OStr "/* not a comment */"
]

end

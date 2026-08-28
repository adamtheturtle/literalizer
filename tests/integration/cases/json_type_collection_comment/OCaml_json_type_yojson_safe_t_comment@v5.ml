module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("a", `Int 1);  (* About a. *)
    ("b", `Int 2)
]

end

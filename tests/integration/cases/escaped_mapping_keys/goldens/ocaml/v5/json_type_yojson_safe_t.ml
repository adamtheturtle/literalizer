module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("quote\"backslash\\", `Int 1);
    ("line\nbreak", `Int 2);
    ("$(literal)${text}", `Int 3);
    ("RStr prefix", `Int 4)
]

end

module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("a", `Intlit "9223372036854775807");
    ("b", `Intlit "9223372036854775808")
]

end

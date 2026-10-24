module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("outer", `List [`List [`String "nested first line\n  indented\n\nnested last line\n"]])
]

end

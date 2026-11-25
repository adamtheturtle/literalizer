module Check = struct

let my_data : Yojson.Safe.t = `List [
    `List [`String "\nfirst line\n  indented\n\nlast line\n"]
]

end

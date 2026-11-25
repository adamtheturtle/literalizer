module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "prefix ${HOME} suffix";
    `String "${interpolated}"
]

end

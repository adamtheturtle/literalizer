module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.";
    `Int 1
]

end

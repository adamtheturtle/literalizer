pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("scores", GDict([#("1", GStr("first")), #("2", GStr("second"))])),
  ])
  let _ = my_data
}

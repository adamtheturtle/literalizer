pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("k", GStr("07:30:00"))])),
    #("b", GDict([#("k", GStr("string"))])),
  ])
  let _ = my_data
}

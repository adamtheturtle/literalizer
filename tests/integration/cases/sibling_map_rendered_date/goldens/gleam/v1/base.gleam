pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("k", GStr("2020-01-01"))])),
    #("b", GDict([#("k", GStr("string"))])),
  ])
  let _ = my_data
}

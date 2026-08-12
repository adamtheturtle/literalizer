pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("value", GDict([#("$ref", GStr("foo"))])),
  ])
  let _ = my_data
}

pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("b", GDict([#("c", GDict([#("$ref", GStr("deep"))]))]))])),
  ])
  let my_data = GDict([
    #("a", GDict([#("b", GDict([#("c", GDict([#("$ref", GStr("deep"))]))]))])),
  ])
  let _ = my_data
}

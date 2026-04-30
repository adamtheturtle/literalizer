pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("$ref", GStr("myVar")),
  ])
  let my_data = GDict([
    #("$ref", GStr("myVar")),
  ])
  let _ = my_data
}

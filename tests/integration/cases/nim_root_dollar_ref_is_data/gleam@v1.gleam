pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("$ref", GStr("schema.json")),
  ])
  let _ = my_data
}

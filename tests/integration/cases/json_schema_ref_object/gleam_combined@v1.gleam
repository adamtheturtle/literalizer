pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("schema", GDict([#("$ref", GStr("#/defs/Foo"))])),
  ])
  let my_data = GDict([
    #("schema", GDict([#("$ref", GStr("#/defs/Foo"))])),
  ])
  let _ = my_data
}

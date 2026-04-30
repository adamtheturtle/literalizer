pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("$ref", GStr("my_var")),
  ])
  let my_data = GDict([
    #("$ref", GStr("my_var")),
  ])
  let _ = my_data
}

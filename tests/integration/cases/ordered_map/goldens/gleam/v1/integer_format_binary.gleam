pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(0b11110)),
    #("active", GBool(True)),
  ])
  let _ = my_data
}

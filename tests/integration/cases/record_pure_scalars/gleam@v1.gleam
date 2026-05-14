pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GFloat(4.5)),
  ])
  let _ = my_data
}

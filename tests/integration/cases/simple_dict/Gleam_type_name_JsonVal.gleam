pub type JsonVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GDict(List(#(String, JsonVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("age", GInt(30)),
    #("active", GBool(True)),
    #("score", GNull),
  ])
  let _ = my_data
}

pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("id", GInt(1)),
    #("owner", GDict([#("name", GStr("Alice")), #("age", GInt(30))])),
  ])
  let _ = my_data
}

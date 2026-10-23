pub type GVal {
  GNull
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("score", GNull),
    #("age", GInt(0b11110)),
  ])
  let _ = my_data
}

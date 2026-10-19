pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("main", GDict([#("x", GInt(1)), #("y", GStr("s"))])),
  ])
  let _ = my_data
}

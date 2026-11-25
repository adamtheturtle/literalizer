pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("k", GInt(1))])),
    #("b", GDict([#("k", GStr("s"))])),
  ])
  let _ = my_data
}

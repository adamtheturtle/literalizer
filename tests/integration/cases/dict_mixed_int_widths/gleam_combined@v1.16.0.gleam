pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GInt(3000000000)),
    #("c", GStr("x")),
  ])
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GInt(3000000000)),
    #("c", GStr("x")),
  ])
  let _ = my_data
}

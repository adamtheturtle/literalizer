pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("v", GStr("ab")),
    #("ab", GInt(1)),
  ])
  let _ = my_data
}

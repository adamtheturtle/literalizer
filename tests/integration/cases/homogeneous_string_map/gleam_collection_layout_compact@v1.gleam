pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GStr("x")),
    #("b", GStr("y")),
  ])
  let _ = my_data
}

pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("x", GStr("before\u{0000}after")),
  ])
  let _ = my_data
}

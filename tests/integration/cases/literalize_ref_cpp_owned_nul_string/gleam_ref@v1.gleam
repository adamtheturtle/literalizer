pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared = GStr("a\u{0000}b")
  let my_data = GDict([
    #("value", shared),
  ])
  let _ = my_data
}

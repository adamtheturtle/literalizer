pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("v", GStr("a‪\u{0000}é😀b")),
  ])
  let _ = my_data
}

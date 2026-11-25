pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("x", GStr("\u{0000}")),
    #("y", GStr("\u{0000}1")),
  ])
  let _ = my_data
}

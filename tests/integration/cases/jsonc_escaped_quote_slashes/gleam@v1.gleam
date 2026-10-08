pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("text", GStr("a\"//b")),
  ])
  let _ = my_data
}

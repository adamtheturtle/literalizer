pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("x", GStr("=")),
    // unrelated
  ])
  let _ = my_data
}

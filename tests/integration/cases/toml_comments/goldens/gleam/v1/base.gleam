pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // before
    #("answer", GInt(42)),  // inline
    #("plain", GStr("ok")),
    // trailing
  ])
  let _ = my_data
}

pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("text", GStr("Record0(")),
    #("number", GInt(0b1)),
  ])
  let _ = my_data
}

pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("line1\r\nline2"),
    GStr("line1\rline2"),
    GStr(""),
  ])
  let _ = my_data
}

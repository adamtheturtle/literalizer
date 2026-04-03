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
    GStr("C:\\path\\to\\file"),
    GStr("back\\\\slash"),
    GStr("hello \\\"world\\\""),
    GStr("path\\to \"# file"),
    GStr("trailing\\"),
    GStr("both \"quotes''' here"),
    GStr("line1\\nline2\nwith newline"),
  ])
  let _ = my_data
}

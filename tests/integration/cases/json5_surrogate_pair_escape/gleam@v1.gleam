pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("astral", GStr("😀")),
    #("mixed", GStr("a😀b")),
    #("count", GInt(2)),
    #("list", GList([GStr("😀"), GInt(1)])),
    #("nested", GDict([#("inner", GStr("😀"))])),
  ])
  let _ = my_data
}

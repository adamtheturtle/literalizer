pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("left", GList([GInt(1), GStr("one")])),
    #("right", GList([GInt(2), GStr("two")])),
  ])
  let _ = my_data
}

pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GList([GList([GInt(1), GStr("value")]), GList([])])),
    #("second", GList([GList([]), GList([GInt(2), GStr("other")])])),
  ])
  let _ = my_data
}

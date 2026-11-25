pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("lint", GList([GInt(2), GList([])])),
    #("test", GList([GInt(5), GList([GStr("compile")])])),
  ])
  let _ = my_data
}

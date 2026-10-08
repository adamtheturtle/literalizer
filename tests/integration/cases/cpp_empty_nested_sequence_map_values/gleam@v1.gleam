pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("alpha", GList([GInt(2), GList([])])),
    #("beta", GList([GInt(5), GList([GStr("x")])])),
  ])
  let _ = my_data
}

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
  let my_data = GDict([
    #("lint", GList([GInt(2), GList([GInt(1)])])),
    #("test", GList([GInt(5), GList([GInt(7)])])),
  ])
  let my_data = GDict([
    #("lint", GList([GInt(2), GList([GInt(1)])])),
    #("test", GList([GInt(5), GList([GInt(7)])])),
  ])
  let _ = my_data
}

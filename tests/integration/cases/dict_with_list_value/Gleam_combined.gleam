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
    #("name", GStr("Alice")),
    #("scores", GList([GInt(10), GInt(20), GInt(30)])),
  ])
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("scores", GList([GInt(10), GInt(20), GInt(30)])),
  ])
  let _ = my_data
}

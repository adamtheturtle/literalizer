pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("scores", GList([GInt(10), GInt(20), GInt(30)])),
    #("args", GList([GInt(1), GStr("email"), GStr("a@gmail.com"), GInt(100)])),
  ])
  let my_data = GDict([
    #("scores", GList([GInt(10), GInt(20), GInt(30)])),
    #("args", GList([GInt(1), GStr("email"), GStr("a@gmail.com"), GInt(100)])),
  ])
  let _ = my_data
}

pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("call", GStr("send")),
    #("args", GList([GInt(1), GStr("email"), GStr("a@gmail.com"), GInt(100)])),
  ])
  let _ = my_data
}

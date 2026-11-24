pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("call", GStr("send")), #("args", GList([GInt(1), GStr("email"), GStr("a@gmail.com"), GInt(100)]))]),
    GDict([#("call", GStr("recv")), #("args", GList([GInt(2), GStr("sms"), GStr("b@example.com"), GInt(200)]))]),
  ])
  let _ = my_data
}

pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([GStr("x")])),
    #("b", GList([GStr("y")])),
  ])
  let _ = my_data
}

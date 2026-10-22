pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("filled", GList([GInt(1), GStr("value")])),
    #("empty", GList([])),
  ])
  let _ = my_data
}

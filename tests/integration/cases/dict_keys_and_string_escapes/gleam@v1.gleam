pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("plain", GList([GInt(1), GInt(2)])),
    #("with-dash", GStr("a\nb")),
  ])
  let _ = my_data
}

pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("test", GList([GInt(5), GList([GStr("compile"), GStr("test")])])),
    #("package", GList([GInt(7), GList([GStr("link"), GStr("test")])])),
  ])
  let _ = my_data
}

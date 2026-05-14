pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("id", GInt(1)),
    #("description", GStr("example")),
    #("is_done", GBool(False)),
    #("blocks", GList([GInt(1), GInt(2), GInt(3)])),
  ])
  let _ = my_data
}

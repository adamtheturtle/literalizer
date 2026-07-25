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
    #("label", GStr("She said \"hello\", then waved")),
    #("enabled", GBool(False)),
    #("related_ids", GList([GInt(1), GInt(2), GInt(3)])),
  ])
  let my_data = GDict([
    #("id", GInt(1)),
    #("label", GStr("She said \"hello\", then waved")),
    #("enabled", GBool(False)),
    #("related_ids", GList([GInt(1), GInt(2), GInt(3)])),
  ])
  let _ = my_data
}

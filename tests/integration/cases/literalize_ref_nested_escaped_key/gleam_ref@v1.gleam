pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let foo = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GDict([
    #("mapping", GDict([#("value", foo)])),
    #("items", GList([GDict([#("other", GInt(1))]), foo])),
  ])
  let _ = my_data
}

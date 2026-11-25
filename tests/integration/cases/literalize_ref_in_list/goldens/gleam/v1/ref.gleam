pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let val_x = GDict([
    #("_", GStr("_")),
  ])
  let val_y = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GList([
    val_x,
    val_y,
  ])
  let _ = my_data
}

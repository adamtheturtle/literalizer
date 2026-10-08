pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let external_value = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GList([
    external_value,
  ])
  let _ = my_data
}

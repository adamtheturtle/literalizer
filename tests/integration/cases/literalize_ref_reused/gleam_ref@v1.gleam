pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared_var = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GList([
    shared_var,
    shared_var,
  ])
  let _ = my_data
}

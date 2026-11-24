pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("mixed", GList([GList([GStr("09:30:00")]), GList([])])),
  ])
  let _ = my_data
}

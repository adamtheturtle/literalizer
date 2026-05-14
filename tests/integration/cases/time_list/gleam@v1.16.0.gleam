pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("times", GList([GStr("09:30:00"), GStr("17:45:00"), GStr("23:59:59")])),
  ])
  let _ = my_data
}

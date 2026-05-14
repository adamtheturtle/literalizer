pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("title", GStr("report")),
    #("tags", GList([GStr("draft"), GStr("urgent"), GStr("review")])),
    #("priority", GInt(2)),
  ])
  let my_data = GDict([
    #("title", GStr("report")),
    #("tags", GList([GStr("draft"), GStr("urgent"), GStr("review")])),
    #("priority", GInt(2)),
  ])
  let _ = my_data
}

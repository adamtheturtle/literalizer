pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("stamps", GList([GStr("2001-02-03T04:05:06+00:00:01"), GStr("2001-02-03T04:05:06-00:00:01"), GStr("2001-02-03T04:05:06+00:00:00.000001"), GStr("2001-02-03T04:05:06-00:00:00.000001"), GStr("2001-02-03T04:05:06+05:30:15.000001"), GStr("2001-02-03T04:05:06-05:30:15.000001")])),
  ])
  let _ = my_data
}

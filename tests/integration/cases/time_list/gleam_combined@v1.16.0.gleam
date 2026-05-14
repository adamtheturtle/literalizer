pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("times", GList(["09:30:00", "17:45:00", "23:59:59"])),
  ])
  let my_data = GDict([
    #("times", GList(["09:30:00", "17:45:00", "23:59:59"])),
  ])
  let _ = my_data
}

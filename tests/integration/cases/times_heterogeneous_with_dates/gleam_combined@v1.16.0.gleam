pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("vals", GList([GStr("2024-01-15"), "09:30:00"])),
  ])
  let my_data = GDict([
    #("vals", GList([GStr("2024-01-15"), "09:30:00"])),
  ])
  let _ = my_data
}

pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("morning", GStr("09:30:00")),
    #("afternoon", GStr("14:15:00")),
    #("evening", GStr("23:59:59")),
  ])
  let _ = my_data
}

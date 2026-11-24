pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("starts_at", GStr("09:30:00")),
  ])
  let _ = my_data
}

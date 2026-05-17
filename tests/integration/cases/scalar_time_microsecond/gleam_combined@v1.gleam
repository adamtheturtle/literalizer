pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("exact_millisecond", GStr("09:30:15.123000")),
    #("sub_millisecond", GStr("09:30:15.123456")),
  ])
  let my_data = GDict([
    #("exact_millisecond", GStr("09:30:15.123000")),
    #("sub_millisecond", GStr("09:30:15.123456")),
  ])
  let _ = my_data
}

pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("half", GStr("1979-05-27T07:32:00.500000")),
    #("milli", GStr("1979-05-27T07:32:00.100000")),
    #("max_milli", GStr("1979-05-27T07:32:00.999000")),
    #("whole", GStr("1979-05-27T07:32:00")),
  ])
  let _ = my_data
}

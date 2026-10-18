pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("before_date", GStr("1582-10-04")),
    #("gap_date", GStr("1582-10-10")),
    #("transition_date", GStr("1582-10-15")),
    #("after_date", GStr("1582-10-16")),
    #("before_naive", GStr("1582-10-04T12:30:00.000001")),
    #("gap_naive", GStr("1582-10-10T12:30:00.500000")),
    #("transition_positive", GStr("1582-10-15T00:30:00+18:00")),
    #("transition_negative", GStr("1582-10-15T23:30:00-18:00")),
    #("after_positive", GStr("1582-10-16T00:30:00+18:00")),
  ])
  let _ = my_data
}

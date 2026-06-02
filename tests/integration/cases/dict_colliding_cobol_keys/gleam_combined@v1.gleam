pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("user_name", GInt(1)),
    #("user.name", GInt(2)),
    #("user-name", GInt(3)),
    #("field_name_that_is_really_quite_long_one", GInt(4)),
    #("field_name_that_is_really_quite_long_two", GInt(5)),
  ])
  let my_data = GDict([
    #("user_name", GInt(1)),
    #("user.name", GInt(2)),
    #("user-name", GInt(3)),
    #("field_name_that_is_really_quite_long_one", GInt(4)),
    #("field_name_that_is_really_quite_long_two", GInt(5)),
  ])
  let _ = my_data
}

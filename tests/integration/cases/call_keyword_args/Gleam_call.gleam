pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  print(throttler.check(user_id: GStr("user_1"), ts: GFloat(1000.0)))
  print(throttler.check(user_id: GStr("user_2"), ts: GFloat(2000.5)))
  let _ = my_data
}

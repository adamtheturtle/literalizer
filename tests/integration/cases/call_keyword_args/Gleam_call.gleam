pub type GVal {
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
}
pub fn throttler_check(_user_id: a, _ts: b) -> Nil { panic }
pub fn emit(__arg: a) -> Nil { panic }

pub fn main() {
  emit(throttler_check(GStr("user_1"), GFloat(1000.0)))
  emit(throttler_check(GStr("user_2"), GFloat(2000.5)))
}

pub type GVal0 {
  GVal0(ancient_date: String, modern_date: String, before_date: String, gap_date: String, transition_date: String, after_date: String, before_naive: String, gap_naive: String, transition_positive: String, transition_negative: String, after_positive: String)
}

pub fn main() {
  let my_data = GVal0(
    ancient_date: "1500-03-01",
    modern_date: "2024-01-15",
    before_date: "1582-10-04",
    gap_date: "1582-10-10",
    transition_date: "1582-10-15",
    after_date: "1582-10-16",
    before_naive: "1582-10-04T12:30:00.000001",
    gap_naive: "1582-10-10T12:30:00.500000",
    transition_positive: "1582-10-15T00:30:00+18:00",
    transition_negative: "1582-10-15T23:30:00-18:00",
    after_positive: "1582-10-16T00:30:00+18:00",
  )
  let _ = my_data
}

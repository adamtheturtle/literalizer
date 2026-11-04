struct Record0 { let positive: Double; let negative: Double; let nan_value: Double; let finite: Double }
let my_data = Record0(
    positive: Double.infinity,
    negative: -Double.infinity,
    nan_value: Double.nan,
    finite: 1.5,
)

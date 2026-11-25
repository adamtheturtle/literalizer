class Capture_ {
    construct new() {}
    call(nan_value, positive_infinity, negative_infinity, finite_value, date_value, datetime_value, text_value) {}
}
var capture = Capture_.new()
capture.call((0/0), (1/0), -(1/0), 1.25, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]")

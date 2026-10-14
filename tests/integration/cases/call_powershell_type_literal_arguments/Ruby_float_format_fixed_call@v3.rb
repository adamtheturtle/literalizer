require 'date'
def capture(*a); end
capture(nan_value: Float::NAN, positive_infinity: Float::INFINITY, negative_infinity: -Float::INFINITY, finite_value: 1.250000, date_value: Date.new(2024, 1, 15), datetime_value: Time.utc(2024, 1, 15, 12, 34, 56), text_value: "[ordinary text]")

require 'date'
def capture(*a); end
capture(nan_value: Float::NAN, positive_infinity: Float::INFINITY, negative_infinity: -Float::INFINITY, finite_value: 1.25, date_value: Date.new(2024, 1, 15, Date::GREGORIAN), datetime_value: 1705322096, text_value: "[ordinary text]")

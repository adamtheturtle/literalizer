module Fixture_call_powershell_type_literal_arguments_Crystal_float_format_fixed_call
extend self
def capture(nan_value = nil, positive_infinity = nil, negative_infinity = nil, finite_value = nil, date_value = nil, datetime_value = nil, text_value = nil); 0; end
capture(nan_value: Float64::NAN, positive_infinity: Float64::INFINITY, negative_infinity: -Float64::INFINITY, finite_value: 1.250000, date_value: Time.utc(2024, 1, 15), datetime_value: "2024-01-15T12:34:56", text_value: "[ordinary text]");
end

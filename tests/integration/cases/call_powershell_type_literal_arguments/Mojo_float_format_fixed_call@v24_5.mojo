import std.math
def capture(nan_value: Float64, positive_infinity: Float64, negative_infinity: Float64, finite_value: Float64, date_value: String, datetime_value: String, text_value: String):
    pass
def main():
    capture(std.math.nan[DType.float64](), std.math.inf[DType.float64](), -std.math.inf[DType.float64](), 1.250000, "2024-01-15", "2024-01-15T12:34:56", "[ordinary text]")

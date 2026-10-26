import std.math
def capture(var nan_value: Float64, var positive_infinity: Float64, var negative_infinity: Float64, var finite_value: Float64, var date_value: String, var datetime_value: Int, var text_value: String):
    pass
def main():
    capture(std.math.nan[DType.float64](), std.math.inf[DType.float64](), -std.math.inf[DType.float64](), 1.25, "2024-01-15", 1705322096, "[ordinary text]")

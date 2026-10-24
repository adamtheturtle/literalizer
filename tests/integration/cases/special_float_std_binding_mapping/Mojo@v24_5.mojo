import std.math
def main():
    var std = {
        "nan": std.math.nan[DType.float64](),
        "positive": std.math.inf[DType.float64](),
        "negative": -std.math.inf[DType.float64](),
    }
    _ = std

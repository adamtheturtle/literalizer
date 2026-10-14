using Dates
capture(args...; kwargs...) = nothing
capture(nan_value=NaN, positive_infinity=Inf, negative_infinity=-Inf, finite_value=1.25, date_value="2024-01-15", datetime_value=DateTime(2024, 1, 15, 12, 34, 56), text_value="[ordinary text]")

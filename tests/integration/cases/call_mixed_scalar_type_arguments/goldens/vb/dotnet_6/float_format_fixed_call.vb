Imports System.Collections.Generic
Module Check
    Function capture(nan_value As Object, positive_infinity As Object, negative_infinity As Object, finite_value As Object, date_value As Object, datetime_value As Object, text_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        capture(Double.NaN, Double.PositiveInfinity, Double.NegativeInfinity, 1.250000, New DateOnly(2024, 1, 15), "2024-01-15T12:34:56", "[ordinary text]")
    End Sub
End Module

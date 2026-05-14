Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Double() {
            Double.PositiveInfinity,
            Double.NegativeInfinity,
            Double.NaN
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Double() {
            Double.PositiveInfinity,
            Double.NegativeInfinity,
            Double.NaN
        }
    End Sub
End Module

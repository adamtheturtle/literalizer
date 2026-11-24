Imports System
Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"morning", New TimeOnly(9, 30, 0)},
            {"afternoon", New TimeOnly(14, 15, 0)},
            {"evening", New TimeOnly(23, 59, 59)}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"morning", New TimeOnly(9, 30, 0)},
            {"afternoon", New TimeOnly(14, 15, 0)},
            {"evening", New TimeOnly(23, 59, 59)}
        }
    End Sub
End Module

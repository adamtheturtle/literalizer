Imports System
Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"times", New TimeOnly() {New TimeOnly(9, 30, 0), New TimeOnly(17, 45, 0), New TimeOnly(23, 59, 59)}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"times", New TimeOnly() {New TimeOnly(9, 30, 0), New TimeOnly(17, 45, 0), New TimeOnly(23, 59, 59)}}
        }
    End Sub
End Module

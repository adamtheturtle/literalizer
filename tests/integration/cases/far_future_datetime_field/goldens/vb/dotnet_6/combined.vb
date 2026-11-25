Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"ts", "3000-12-31T23:59:59.999999+00:00"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"ts", "3000-12-31T23:59:59.999999+00:00"}
        }
    End Sub
End Module

Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' Configuration
        ' Port setting
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "app"},
            {"port", 3000}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' Configuration
        ' Port setting
        my_data = New Dictionary(Of String, Object) From {
            {"name", "app"},
            {"port", 3000}
        }
    End Sub
End Module

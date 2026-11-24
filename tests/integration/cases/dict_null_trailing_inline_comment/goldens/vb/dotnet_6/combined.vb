Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' not configured yet
        Dim my_data = New Dictionary(Of String, Object) From {
            {"host", "localhost"},
            {"port", Nothing}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' not configured yet
        my_data = New Dictionary(Of String, Object) From {
            {"host", "localhost"},
            {"port", Nothing}
        }
    End Sub
End Module

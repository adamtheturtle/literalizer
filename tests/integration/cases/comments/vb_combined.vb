Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' Server configuration
        ' default host
        ' Enable debug mode
        Dim my_data = New Dictionary(Of String, Object) From {
            {"host", "localhost"},
            {"port", 8080},
            {"debug", True}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' Server configuration
        ' default host
        ' Enable debug mode
        my_data = New Dictionary(Of String, Object) From {
            {"host", "localhost"},
            {"port", 8080},
            {"debug", True}
        }
    End Sub
End Module

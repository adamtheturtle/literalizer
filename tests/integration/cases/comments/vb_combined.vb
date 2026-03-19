Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            ' Server configuration
            {"host", "localhost"},  ' default host
            {"port", 8080},
            ' Enable debug mode
            {"debug", True}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            ' Server configuration
            {"host", "localhost"},  ' default host
            {"port", 8080},
            ' Enable debug mode
            {"debug", True}
        }
    End Sub
End Module

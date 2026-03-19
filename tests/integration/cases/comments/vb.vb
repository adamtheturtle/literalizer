Imports System.Collections.Generic
Module Check
    Dim x As Object = New Dictionary(Of String, Object) From {
        ' Server configuration
        {"host", "localhost"},  ' default host
        {"port", 8080},
        ' Enable debug mode
        {"debug", True}
    }
End Module

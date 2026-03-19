Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        ' Server configuration
        {"host", "localhost"},  ' default host
        {"port", 8080},
        ' Enable debug mode
        {"debug", True}
    }
End Module

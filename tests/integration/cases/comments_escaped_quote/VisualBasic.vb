Imports System.Collections.Generic
Module Check
    Dim x As Object = ' real
    New Dictionary(Of String, Object) From {
        {"key", "value "" # not a comment"}
    }
End Module

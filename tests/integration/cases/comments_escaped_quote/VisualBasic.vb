Imports System.Collections.Generic
Module Check
    ' real
    Dim my_data As Object = New Dictionary(Of String, Object) From {
        {"key", "value "" # not a comment"}
    }
End Module

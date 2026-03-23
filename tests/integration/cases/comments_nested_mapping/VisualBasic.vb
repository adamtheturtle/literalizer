Imports System.Collections.Generic
Module Check
    Dim x As Object = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"x", 1}}},
        {"b", 2}
    }
End Module

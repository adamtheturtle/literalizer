Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"b", New Dictionary(Of String, Object) From {{"k", 1}}},
        {"a", New Dictionary(Of String, Object) From {{"k", "2040-01-01T00:00:00+00:00"}}}
    }
End Module

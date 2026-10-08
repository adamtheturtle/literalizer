Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"k", 1}}},
        {"b", New Dictionary(Of String, Object) From {{"k", "s"}}}
    }
End Module

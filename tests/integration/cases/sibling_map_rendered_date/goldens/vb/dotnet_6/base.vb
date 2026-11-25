Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"k", New DateOnly(2020, 1, 1)}}},
        {"b", New Dictionary(Of String, Object) From {{"k", "string"}}}
    }
End Module

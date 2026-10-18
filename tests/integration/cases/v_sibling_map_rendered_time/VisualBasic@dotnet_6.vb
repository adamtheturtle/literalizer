Imports System
Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"k", New TimeOnly(7, 30, 0)}}},
        {"b", New Dictionary(Of String, Object) From {{"k", "string"}}}
    }
End Module

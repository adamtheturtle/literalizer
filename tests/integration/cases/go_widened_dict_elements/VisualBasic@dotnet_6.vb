Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Object() {New Dictionary(Of String, Object) From {}, New Dictionary(Of String, Object) From {{"x", 1}}}},
        {"b", New Object() {New Integer() {}, New Integer() {1}}}
    }
End Module

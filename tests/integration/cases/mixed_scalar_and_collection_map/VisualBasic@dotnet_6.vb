Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", 1},
        {"b", "x"},
        {"e", New Integer() {1, 2}},
        {"f", New Dictionary(Of String, Object) From {{"g", "h"}}}
    }
End Module

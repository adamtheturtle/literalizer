Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"plain", New Integer() {1, 2}},
        {"with-dash", "a" & Chr(10) & "b"}
    }
End Module

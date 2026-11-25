Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"items", New Object() {New Dictionary(Of String, Object) From {{"id", 1}}, New Dictionary(Of String, Object) From {{"id", 2}, {"count", 10}}, New Dictionary(Of String, Object) From {{"id", 3}, {"count", 20}}}}
    }
End Module

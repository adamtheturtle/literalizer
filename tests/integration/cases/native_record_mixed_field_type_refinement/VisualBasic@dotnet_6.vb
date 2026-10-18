Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"first", New Dictionary(Of String, Object) From {{"items", New Object() {1, New Dictionary(Of String, Object) From {{"value", 2}}}}}},
        {"second", New Dictionary(Of String, Object) From {{"items", New Object() {1, New Dictionary(Of String, Object) From {{"value", "s"}}}}}}
    }
End Module

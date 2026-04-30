Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"b", New Dictionary(Of String, Object) From {{"c", New Dictionary(Of String, Object) From {{"$ref", "deep"}}}}}}}
    }
End Module

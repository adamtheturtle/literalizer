Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"x", 1}}},
        {"b", 2}
    }
End Module

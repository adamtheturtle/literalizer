Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"b", 1}}},
        {"list", New Integer() {1, 2}}
    }
End Module

Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Object() {}},
        {"b", New HashSet(Of Integer) From {1, 2}}
    }
End Module

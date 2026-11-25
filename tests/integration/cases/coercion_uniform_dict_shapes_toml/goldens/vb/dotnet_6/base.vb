Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"_", New Object() {New Dictionary(Of String, Object) From {{"type", "create"}, {"name", "a"}}, New Dictionary(Of String, Object) From {{"type", "update"}, {"name", "b"}}}}
    }
End Module

Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"rows", New Object() {New Dictionary(Of String, Object) From {{"x", 1}, {"y", "a"}}, New Dictionary(Of String, Object) From {{"x", 2}, {"y", "b"}}}}
    }
End Module

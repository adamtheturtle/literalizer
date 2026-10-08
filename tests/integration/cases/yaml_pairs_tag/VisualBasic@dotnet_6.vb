Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"first", 1}},
        New Dictionary(Of String, Object) From {{"repeated", "a"}},
        New Dictionary(Of String, Object) From {{"repeated", "b"}}
    }
End Module

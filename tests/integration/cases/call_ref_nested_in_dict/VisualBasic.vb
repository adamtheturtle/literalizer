Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Object() {New Dictionary(Of String, Object) From {{"key", New Dictionary(Of String, Object) From {{"$ref", "my_var"}}}, {"count", 42}}}
    }
End Module

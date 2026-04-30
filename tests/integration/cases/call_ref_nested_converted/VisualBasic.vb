Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "myVar"}}, 42, "static"}}
    }
End Module

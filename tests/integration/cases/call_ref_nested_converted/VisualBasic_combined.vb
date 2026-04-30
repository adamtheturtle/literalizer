Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "myVar"}}, 42, "static"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "myVar"}}, 42, "static"}}
        }
    End Sub
End Module

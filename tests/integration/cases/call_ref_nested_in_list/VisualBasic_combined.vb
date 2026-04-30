Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_var"}}, 42, "static"}},
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_other"}}, 7, "label"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_var"}}, 42, "static"}},
            New Object() {New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_other"}}, 7, "label"}}
        }
    End Sub
End Module

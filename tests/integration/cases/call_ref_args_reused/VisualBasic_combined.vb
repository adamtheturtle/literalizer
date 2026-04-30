Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "repeated_var"}}, 1},
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "single_var"}}, 0},
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "repeated_var"}}, 8}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "repeated_var"}}, 1},
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "single_var"}}, 0},
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "repeated_var"}}, 8}
        }
    End Sub
End Module

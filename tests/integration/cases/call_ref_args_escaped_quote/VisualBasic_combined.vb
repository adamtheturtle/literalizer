Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_str"}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"$ref", "my_str"}}}
        }
    End Sub
End Module

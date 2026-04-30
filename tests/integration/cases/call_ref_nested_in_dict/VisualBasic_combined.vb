Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"key", New Dictionary(Of String, Object) From {{"$ref", "my_var"}}}, {"count", 42}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"key", New Dictionary(Of String, Object) From {{"$ref", "my_var"}}}, {"count", 42}}}
        }
    End Sub
End Module

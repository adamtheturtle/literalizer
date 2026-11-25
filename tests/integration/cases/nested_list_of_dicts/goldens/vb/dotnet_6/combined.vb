Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"name", "Alice"}}, New Dictionary(Of String, Object) From {{"name", "Bob"}}},
            New Object() {New Dictionary(Of String, Object) From {{"name", "Charlie"}}, New Dictionary(Of String, Object) From {{"name", "Dave"}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"name", "Alice"}}, New Dictionary(Of String, Object) From {{"name", "Bob"}}},
            New Object() {New Dictionary(Of String, Object) From {{"name", "Charlie"}}, New Dictionary(Of String, Object) From {{"name", "Dave"}}}
        }
    End Sub
End Module

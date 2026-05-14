Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"name", "Alice"}, {"age", 30}},
            New Dictionary(Of String, Object) From {{"name", "Bob"}, {"age", 25}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"name", "Alice"}, {"age", 30}},
            New Dictionary(Of String, Object) From {{"name", "Bob"}, {"age", 25}}
        }
    End Sub
End Module

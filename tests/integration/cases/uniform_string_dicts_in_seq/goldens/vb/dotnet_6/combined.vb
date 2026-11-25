Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"first", "Alice"}, {"last", "Smith"}},
            New Dictionary(Of String, Object) From {{"first", "Bob"}, {"last", "Jones"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"first", "Alice"}, {"last", "Smith"}},
            New Dictionary(Of String, Object) From {{"first", "Bob"}, {"last", "Jones"}}
        }
    End Sub
End Module

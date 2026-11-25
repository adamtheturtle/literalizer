Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' This comment describes the last pair.
        Dim my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"item", "existing"}}, "kept"},
            New Object() {New Dictionary(Of String, Object) From {{"item", "next"}}, "also kept"},
            New Object() {New Dictionary(Of String, Object) From {{"item", "last"}}, "kept too"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' This comment describes the last pair.
        my_data = New Object() {
            New Object() {New Dictionary(Of String, Object) From {{"item", "existing"}}, "kept"},
            New Object() {New Dictionary(Of String, Object) From {{"item", "next"}}, "also kept"},
            New Object() {New Dictionary(Of String, Object) From {{"item", "last"}}, "kept too"}
        }
    End Sub
End Module

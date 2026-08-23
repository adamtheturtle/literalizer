Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' This comment describes the next item.
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"item", "existing"}},
            New Dictionary(Of String, Object) From {{"item", "next"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' This comment describes the next item.
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"item", "existing"}},
            New Dictionary(Of String, Object) From {{"item", "next"}}
        }
    End Sub
End Module

Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {
                {"item", "existing"}
                ' This comment describes the next item.
            },
            New Dictionary(Of String, Object) From {{"item", "next"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {
                {"item", "existing"}
                ' This comment describes the next item.
            },
            New Dictionary(Of String, Object) From {{"item", "next"}}
        }
    End Sub
End Module

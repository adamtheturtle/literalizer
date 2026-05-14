Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New HashSet(Of String) From {"a", "b"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New HashSet(Of String) From {"a", "b"}
        }
    End Sub
End Module

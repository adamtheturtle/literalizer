Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Object() {1, "a"},
            New Object() {2, "b"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Object() {1, "a"},
            New Object() {2, "b"}
        }
    End Sub
End Module

Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Integer() {1, 2},
            New Object() {},
            New String() {"a", "b"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Integer() {1, 2},
            New Object() {},
            New String() {"a", "b"}
        }
    End Sub
End Module

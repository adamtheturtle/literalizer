Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' trailing note
        ' next element
        Dim my_data = New Object() {
            New Object() {2, "hello"},
            New Object() {3, "world"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' trailing note
        ' next element
        my_data = New Object() {
            New Object() {2, "hello"},
            New Object() {3, "world"}
        }
    End Sub
End Module

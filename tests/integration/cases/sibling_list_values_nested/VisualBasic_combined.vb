Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"lint", New Object() {2, New Object() {}}},
            {"test", New Object() {5, New Object() {"compile"}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"lint", New Object() {2, New Object() {}}},
            {"test", New Object() {5, New Object() {"compile"}}}
        }
    End Sub
End Module

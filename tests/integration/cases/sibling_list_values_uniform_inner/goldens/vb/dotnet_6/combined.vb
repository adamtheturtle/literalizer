Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"lint", New Object() {2, New Integer() {1}}},
            {"test", New Object() {5, New Integer() {7}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"lint", New Object() {2, New Integer() {1}}},
            {"test", New Object() {5, New Integer() {7}}}
        }
    End Sub
End Module

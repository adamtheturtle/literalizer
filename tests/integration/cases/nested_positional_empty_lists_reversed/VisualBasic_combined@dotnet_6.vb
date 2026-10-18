Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Integer()() {New Integer() {1}},
            New Object() {New Object() {}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Integer()() {New Integer() {1}},
            New Object() {New Object() {}}
        }
    End Sub
End Module

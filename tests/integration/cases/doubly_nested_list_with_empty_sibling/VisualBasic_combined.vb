Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Integer()()() {
            New Integer()() {New Integer() {1, 2}},
            New Integer()() {},
            New Integer()() {New Integer() {3, 4}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Integer()()() {
            New Integer()() {New Integer() {1, 2}},
            New Integer()() {},
            New Integer()() {New Integer() {3, 4}}
        }
    End Sub
End Module

Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"value", New Integer() {}}},
            New Dictionary(Of String, Object) From {{"value", New Integer() {1}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"value", New Integer() {}}},
            New Dictionary(Of String, Object) From {{"value", New Integer() {1}}}
        }
    End Sub
End Module

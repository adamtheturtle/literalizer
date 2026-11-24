Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"groups", New Object() {New Object() {New Dictionary(Of String, Object) From {{"id", 1}}}, New Object() {New Dictionary(Of String, Object) From {{"id", 2}}}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"groups", New Object() {New Object() {New Dictionary(Of String, Object) From {{"id", 1}}}, New Object() {New Dictionary(Of String, Object) From {{"id", 2}}}}}
        }
    End Sub
End Module

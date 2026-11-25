Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {},
            New Dictionary(Of String, Object) From {}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {},
            New Dictionary(Of String, Object) From {}
        }
    End Sub
End Module

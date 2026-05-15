Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"scores", New Object() {10, 20, 30}},
            {"args", New Object() {1, "email", "a@gmail.com", 100}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"scores", New Object() {10, 20, 30}},
            {"args", New Object() {1, "email", "a@gmail.com", 100}}
        }
    End Sub
End Module

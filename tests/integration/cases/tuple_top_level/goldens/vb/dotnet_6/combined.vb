Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            1,
            "email",
            "a@gmail.com",
            100
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            1,
            "email",
            "a@gmail.com",
            100
        }
    End Sub
End Module

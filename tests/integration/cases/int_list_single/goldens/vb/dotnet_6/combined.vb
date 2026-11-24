Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Integer() {
            1
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Integer() {
            1
        }
    End Sub
End Module

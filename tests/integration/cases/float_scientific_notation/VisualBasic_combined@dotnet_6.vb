Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Double() {
            0.0,
            1.0,
            1500.0,
            0.001
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Double() {
            0.0,
            1.0,
            1500.0,
            0.001
        }
    End Sub
End Module

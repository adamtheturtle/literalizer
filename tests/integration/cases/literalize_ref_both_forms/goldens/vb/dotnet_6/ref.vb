Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim SharedValues = New Integer() {
            1,
            2
        }
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", SharedValues}
        }
    End Sub
    Sub _assignment()
        Dim SharedValues = New Integer() {
            1,
            2
        }
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", SharedValues}
        }
        my_data = New Dictionary(Of String, Object) From {
            {"a", SharedValues}
        }
    End Sub
End Module

Imports System.Collections.Generic
Module Check
    Function consume_widget(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = Nothing
        Dim my_data = Nothing
        consume_widget(my_data)
        my_data = item
        consume_widget(my_data)
    End Sub
End Module

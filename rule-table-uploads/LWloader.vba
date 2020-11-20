Sub LWloader()
    Dim d As New ChromeDriver # requires a reference added to "Selenium Type Library" in Excel
    ' https://github.com/florentbr/SeleniumBasic/releases/tag/v2.0.9.0    
    Dim e As WebElement, f As WebElement 
    Dim strFileContent As String

    filepath = "C:\users\{username}\Desktop\BatchOutput\"
    'Dim keyObj As Selenium.keys
    'Set keyObj = New Selenium.keys
    ' An apparent bug in the Basic Selenium package cases the script
    '   to fail as soon as a Ctrl+V is sent. This would be a much faster
    '   way of pasting text into the edit field than SendKeys,
    '   which is really painfully slow.  But sending Ctrl+V appears
    '   to "stick down" the virtual Control key after the first use,
    '   which makes each Get call produce a result in a new window,
    '   which prevents the script from working.
    ' TODO: try using Selenium package in Python instead of this silly VBA one,
    '       see if it avoids this annoying bug
 
    ' sample rulenames array -- could load these from a file
    rulenames = Array("LifeBellman.rule", "lifebf7.rule", "LifeLayers.rule", "longlast.rule", "lotsofdots.rule", _
"LRW.rule", "MComp.rule", "Mirrors.rule", "Moore2vn-B3S23.rule", "notlife.rule", "PredatorPreyClean.rule", _
"Predator.rule", "QuadLife.rule", "Rainbow.rule", "shapeloop3.rule", "shapeloop-ltd.rule", "SheepNGoats.rule", _
"StateInvestigator.rule", "Symbiosis.rule", "testlife.rule", "test.rule", "TLifeHistory.rule", "TriLifeA.rule", _
"v3k4_fish2.rule", "v3k4_temp.rule", "x-rule-pre.rule")

    ptr = 0
    d.Start "chrome"
    d.Get "https://conwaylife.com/wiki/"
    d.Window().Maximize
    d.FindElementByLinkText("Log in").Click
    d.Wait 1000
    d.FindElementById("wpName1").Click
    d.SendKeys ("{username}")
    d.FindElementById("wpPassword1").Click
    d.SendKeys ("{password}")
    d.FindElementById("wpRemember").Click
    d.FindElementById("wpLoginAttempt").Click
    d.Wait 1000
    
    Do While ptr <= UBound(rulenames, 1)
        rulename = rulenames(ptr)
        ptr = ptr + 1
        Dim iFile As Integer: iFile = FreeFile
        Open filepath & rulename For Input As #iFile
        strFileContent = Input(LOF(iFile), iFile)
        Close #iFile
        Do While Right(strFileContent, 1) = Chr(10) Or Right(strFileContent, 1) = Chr(13)
            strFileContent = Left(strFileContent, Len(strFileContent) - 1)
        Loop
        
        'd.Get "https://conwaylife.com/wiki/Rule:" + Left(rulename, Len(rulename) - 5)
        
        'd.FindElementByLinkText("create this page").Click
        'd.Wait 2000
        d.Get "https://conwaylife.com/w/index.php?title=Rule:" & Left(rulename, Len(rulename) - 5) & "&action=edit"
        skipthisone = 0
        If Len(strFileContent) > 2048000 Then skipthisone = 1
        Set e = d.FindElementByLinkText("help page", 10000, False) ' will fail if there's already text on the page
        If e Is Nothing Then
            MsgBox ("There is already an article for rule '" & rulename & "'.")
            skipthisone = 1
        End If
        If skipthisone = 0 Then
            d.FindElementById("wpSummary").Click
            d.SendKeys ("Rule '" & Left(rulename, Len(rulename) - 5) & "' from auto-import project")
            
            d.FindElementById("wpTextbox1").Click
            ' d.SendKeys (strFileContent)
            d.SetClipBoard strFileContent
            If Len(strFileContent) > 25000 Then
            
                MsgBox ("Please paste clipboard contents, then click OK here.")
            Else
                d.SendKeys (strFileContent)
            End If
            'd.SendKeys keyObj.Control & "v"  ' d.SendKeys (strFileContent) ' (much slower, over 100 seconds for long text, causes timeout)
            ' MsgBox ("OK?")
            'Exit Sub
            d.FindElementById("wpSave").Click
            d.Wait (2000)
        End If
    Loop

End Sub

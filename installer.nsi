!include "MUI2.nsh"
!include "x64.nsh"

Name "DrawRunes"
OutFile "DrawRunes-Installer.exe"
InstallDir "$PROGRAMFILES\DrawRunes"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Extract files
  File /r "dist\drawrunes\libs"
  FILE /r "dist\drawrunes\Runes"
  File "dist\drawrunes\readme.md"
  File "dist\drawrunes\LICENSE"
  File "dist\drawrunes\drawrunes.exe"
  
  ; Add to PATH using registry
  SetRegView 64
  
  ReadRegStr $0 HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "PATH"
  ${If} $0 != ""
    StrCpy $0 "$0;$INSTDIR"
  ${Else}
    StrCpy $0 "$INSTDIR"
  ${EndIf}
  WriteRegStr HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment" "PATH" $0
  
  ; Notify system of PATH change
  SendMessage ${HWND_BROADCAST} ${WM_SETTINGCHANGE} 0 "STR:Environment" /TIMEOUT=5000
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\DrawRunes"
  CreateShortCut "$SMPROGRAMS\DrawRunes\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  ; Remove files
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\DrawRunes"
SectionEnd
!include "MUI2.nsh"
!include "x64.nsh"

Name "DrawRunes"
  
; Add Icons
Icon "dist\drawrunes\DrawRunes.ico"
UninstallIcon "dist\drawrunes\DrawRunes.ico"

OutFile "dist\DrawRunes-Installer.exe"
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
  File "dist\drawrunes\LICENSE.md"
  File "dist\drawrunes\drawrunes.exe"
  File "dist\drawrunes\DrawRunes.ico"
  
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
  CreateShortCut "$SMPROGRAMS\DrawRunes\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\DrawRunes.ico"
  CreateShortCut "$SMPROGRAMS\DrawRunes\DrawRunes.lnk" "$INSTDIR\drawrunes.exe" "" "$INSTDIR\DrawRunes.ico"
  
SectionEnd

Section "Uninstall"
  ; Remove files
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\DrawRunes"
SectionEnd
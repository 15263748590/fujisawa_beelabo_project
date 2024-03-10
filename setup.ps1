# pythonがインストールされているかチェックする関数
function Check-Python {
    try {
        python --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# npmがインストールされているかチェックする関数
function Check-Npm {
    try {
        npm --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# pythonをインストールする関数
function Install-Python {
    # pythonのインストーラーをダウンロードする
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe" -OutFile "python-installer.exe"

    # pythonをインストールする
    .\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    # インストーラーを削除する
    Remove-Item -Path "python-installer.exe"
}

# npmをインストールする関数
function Install-Npm {
    # Node.jsのインストーラーをダウンロードする
    Invoke-WebRequest -Uri "https://nodejs.org/dist/v14.17.0/node-v14.17.0-x64.msi" -OutFile "node-installer.msi"

    # Node.jsをインストールする（npmも一緒にインストールされる）
    msiexec.exe /i "node-installer.msi" /qn

    # インストーラーを削除する
    Remove-Item -Path "node-installer.msi"
}

# メインの処理
# frontendディレクトリに移動する
Set-Location -Path "frontend"

# npmがインストールされていない場合はインストールする
if (!(Check-Npm)) {
    Install-Npm
}

# npm installを実行する
npm install

# backendディレクトリに移動する
Set-Location -Path "..\backend"

# pythonがインストールされていない場合はインストールする
if (!(Check-Python)) {
    Install-Python
}

# uvicorn main:app --reloadを実行する
uvicorn main:app --reload
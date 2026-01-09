# gu-s26-math5310
Georgetown University Spring 2026 MATH5310 Deep Learning Sample Files

# Setup 
Connect to SaxaNet Secure Wireless
  https://uis.georgetown.edu/saxanet/

Install Git
  https://git-scm.com/

Install Podman
  https://podman.io/

Install a programmer's text editor
  * Mac: BBEdit
  * Windows: Notepad++  
  * Linux: Geany
  * Any OS: VSCode  https://code.visualstudio.com/download

(Windows Only): Install Windows Subsystem for Linux (WSL)
  * Open PowerShell as Administrator
    * Start > "Powershell" > click "Run As Administrator..."
  * wsl --install
  * Close Powershell
  * Launch WSL
    * Start > "WSL"

# One-time Setup

Then, for all systems, from your CLI (Terminal, term, iTerm, WSL, ... *not* Powershell)
```
  podman machine list     # optional to see there's no default machine
  podman machine init     # one-time step
  podman machine list     # optional to confirm the machine creation

  # Use your name and GU NetID  
  git config --global user.name 'Your Name'
  git config --global user.email your_netid@georgetown.edu
  git config --global core.autocrlf input

  # You might wish to create or already have a preferred parent directory
  # If so, CD into that directory now

  git clone https://github.com/WilDoane/gu-s26-math5310.git

  cd gu-s26-math5310

  podman images # to see there are no images yet
  
  podman machine start

  sed 's/\r$//' build.sh | . /dev/stdin
  
  podman images # to see the downloaded and built images
```

# Typical Work Session
  
From your CLI (Terminal, term, iTerm, WSL, ... *not* Powershell)
```
  podman machine start
  
  cd gu-s26-math5310
  git pull
  
  sed 's/\r$//' run.sh | . /dev/stdin

  # Visit the URL offered (along with the token)
  
  # CTRL-C to terminate session
  
  podman machine stop
```    

The `workspace` directory is shared between your host OS and the guest Linux OS this process installs. Files you create, modify, or delete are the same both in the VM and on your host OS. That implies you could use a text editor from either environment for editing code files, ad that you can copy files from that directory into an email or Canvas.

  
# Clean Up

In the event you want to remove this setup completely:

From your CLI (Terminal, term, iTerm, WSL, ... *not* Powershell)
```
podman machine start
podman image rm -f dl-cpu
podman image rm python3.11
podman machine stop
podman machine rm podman-machine-default
```

Then, use your OS's method for uninstalling git and podman (e.g., on Windows, Start > Add or Remove Programs).

If you want to remove traces of this repository from your system, you would also need to delete the cloned directory: gu-s26-math5310.


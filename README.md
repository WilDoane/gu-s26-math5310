# gu-s26-math5310
Georgetown University Spring 2026 MATH5310 Deep Learning Sample Files

# Setup 
Connect to SaxaNet Secure Wireless
  https://uis.georgetown.edu/saxanet/

Install Git
  https://git-scm.com/

Install Podman
  https://podman.io/
  
From your CLI
```
  # One-time Setup
  
  podman machine init     # one-time step
  podman machine list     # optional

  # Use your name and NetID  
  git config --global user.name 'William Doane'
  git config --global user.email wd394@georgetown.edu

  # You might wish to create or already have a preferred parent directory
  git clone https://github.com/WilDoane/gu-s26-math5310.git

  cd gu-s26-math5310
  git pull
  
  podman machine start
  . ./build.sh
  
  podman images
```

# Typical Work Session
  
```
  podman machine start
  
  cd gu-s26-math5310
  git pull
  
  . ./run.sh

  # Visit the URL offered (along with the token)
  
  # CTRL-C to terminate session
  
  podman machine stop
```    
  
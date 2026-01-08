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
  
  podman machine list     # optional to see there's no default machine
  podman machine init     # one-time step
  podman machine list     # optional to confirm the machine creation

  # Use your name and GU NetID  
  git config --global user.name 'Your Name'
  git config --global user.email your_netid@georgetown.edu

  # You might wish to create or already have a preferred parent directory
  # If so, CD into that directory now

  git clone https://github.com/WilDoane/gu-s26-math5310.git

  cd gu-s26-math5310

  podman images # to see there are no images yet
  
  podman machine start

  . ./build.sh
  
  podman images # to see the downloaded and built images
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
  

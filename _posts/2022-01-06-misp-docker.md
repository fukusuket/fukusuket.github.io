---
layout: post
title:  "MISPのDockerインストールでエラー"
date:   2022-01-06
---


## 環境情報

- M1 Mac


## 再現手順

- README通り、実行
  - https://github.com/misp/misp-docker#building-your-image

## エラー

```
> docker-compose build
db uses an image, skipping
Building web
[+] Building 83.5s (15/23)                                                                                                                                    
 => [internal] load build definition from Dockerfile                                                                                                     0.0s
 => => transferring dockerfile: 2.59kB                                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                                                                         3.4s
 => [internal] load build context                                                                                                                        0.0s
 => => transferring context: 136.38kB                                                                                                                    0.0s
 => [ 1/19] FROM docker.io/library/ubuntu:latest@sha256:b5a61709a9a44284d88fb12e5c48db0409cfad5b69d4ff8224077c57302df9cf                                 1.4s
 => => resolve docker.io/library/ubuntu:latest@sha256:b5a61709a9a44284d88fb12e5c48db0409cfad5b69d4ff8224077c57302df9cf                                   0.0s
 => => sha256:64162ac111b666daf1305de1888eb67a3033f62000f5ff781fe529aff8f88b09 529B / 529B                                                               0.0s
 => => sha256:9f4877540c734dfd8ee2e523b1487788f871e64a4f3137797d33e5971ac9adde 1.48kB / 1.48kB                                                           0.0s
 => => sha256:5f3d23ccb99f6c9462a15efcf35aef0863858073a06d56df671d0e791b26222a 27.17MB / 27.17MB                                                         0.7s
 => => sha256:b5a61709a9a44284d88fb12e5c48db0409cfad5b69d4ff8224077c57302df9cf 1.42kB / 1.42kB                                                           0.0s
 => => extracting sha256:5f3d23ccb99f6c9462a15efcf35aef0863858073a06d56df671d0e791b26222a                                                                0.7s
 => [ 2/19] RUN apt-get update &&     apt-get dist-upgrade -y && apt-get upgrade && apt-get autoremove -y && apt-get clean &&     apt-get install -y s  53.1s
 => [ 3/19] RUN add-apt-repository ppa:deadsnakes/ppa                                                                                                    7.8s
 => [ 4/19] RUN apt-get update && apt-get -y install python3.9 python3-pip                                                                              13.6s 
 => [ 5/19] RUN pip3 install --upgrade pip                                                                                                               2.4s 
 => [ 6/19] RUN locale-gen en_US.UTF-8                                                                                                                   1.0s 
 => [ 7/19] RUN useradd misp && usermod -aG sudo misp                                                                                                    0.3s 
 => [ 8/19] COPY --chown=misp:misp INSTALL_NODB.sh* ./                                                                                                   0.0s 
 => [ 9/19] RUN chmod +x INSTALL_NODB.sh                                                                                                                 0.1s 
 => [10/19] RUN echo "ALL ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers                                                                                       0.1s 
 => ERROR [11/19] RUN bash INSTALL_NODB.sh -A -u                                                                                                         0.3s 
------                                                                                                                                                        
 > [11/19] RUN bash INSTALL_NODB.sh -A -u:                                                                                                                    
#15 0.207 sha1 matches                                                                                                                                        
#15 0.220 sha256 matches                                                                                                                                      
#15 0.231 sha384 matches                                                                                                                                      
#15 0.243 sha512 matches                                                                                                                                      
#15 0.244 tput: No value for $TERM and no -T specified
#15 0.244 -
#15 0.253 The following DB Passwords were generated...
#15 0.253 Admin (root) DB Password: cde2bcf451ed82b56638d108beb7f544dc6f816a46644f7a2887eba0c50d2276
#15 0.253 User  (misp) DB Password: 997a75fe154b0fa1ec966b5570ffbf9ba44378ad60ff2cc351d06164d8848df9
#15 0.253 all
#15 0.253 unattended
#15 0.256     Either your platform is not easily detectable or is not supported by this
#15 0.256     installer script.
#15 0.256     Please visit the following URL for more detailed installation instructions:
#15 0.256     https://misp.github.io/MISP/
------
executor failed running [/bin/sh -c bash INSTALL_NODB.sh -A -u]: exit code: 1
ERROR: Service 'web' failed to build : Build failed
```

## 調査

- uname -m の結果はaarch64
- Ubuntu20.04LTS上のDockerで発生しない

## 対処

- Install.shのOS判定処理でコケるので、ここ修正
  - https://github.com/MISP/misp-docker/blob/master/web/INSTALL_NODB.sh
  
## 参考

- [MISP/misp-docker](https://github.com/MISP/misp-docker)

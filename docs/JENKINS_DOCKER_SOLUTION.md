# Jenkins Docker 镜像拉取解决方案

## 问题原因
1. Docker Desktop 可能还在启动中
2. 网络连接问题
3. 镜像源配置问题

## 解决方案
1. 等待Docker Desktop完全启动（30-60秒）
2. 尝试拉取其他版本: docker pull jenkins/jenkins:lts
3. 使用您项目中已配置的本地Jenkins

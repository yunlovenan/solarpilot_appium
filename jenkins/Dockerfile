FROM jenkins/jenkins:lts-jdk17

USER root

# 安装必要的包
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    git \
    lib32stdc++6 \
    lib32z1 \
    lib32ncurses5 \
    lib32bz2-1.0 \
    libc6-dev \
    g++ \
    make \
    cmake \
    pkg-config \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/emulator
ENV PATH=$PATH:$ANDROID_HOME/tools
ENV PATH=$PATH:$ANDROID_HOME/tools/bin
ENV PATH=$PATH:$ANDROID_HOME/platform-tools
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# 创建Android SDK目录
RUN mkdir -p $ANDROID_HOME

# 下载并安装Android Command Line Tools
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip \
    && unzip -q commandlinetools-linux-10406996_latest.zip -d /tmp \
    && mkdir -p $ANDROID_HOME/cmdline-tools \
    && mv /tmp/cmdline-tools $ANDROID_HOME/cmdline-tools/latest \
    && rm commandlinetools-linux-10406996_latest.zip

# 接受Android SDK许可
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

# 安装Android SDK组件
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-33" \
    "platforms;android-32" \
    "platforms;android-31" \
    "platforms;android-30" \
    "build-tools;33.0.0" \
    "build-tools;32.0.0" \
    "build-tools;31.0.0" \
    "build-tools;30.0.3" \
    "system-images;android-33;google_apis;x86_64" \
    "system-images;android-32;google_apis;x86_64" \
    "system-images;android-31;google_apis;x86_64" \
    "emulator" \
    "extras;intel;Hardware_Accelerated_Execution_Manager"

# 创建AVD（Android Virtual Device）
RUN echo "no" | $ANDROID_HOME/cmdline-tools/latest/bin/avdmanager create avd \
    -n "test_device" \
    -k "system-images;android-33;google_apis;x86_64" \
    --force

# 安装Node.js和npm（用于Appium）
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 安装Appium
RUN npm install -g appium@latest

# 安装Python依赖
RUN pip3 install --no-cache-dir \
    pytest \
    pytest-html \
    allure-pytest \
    requests \
    selenium

# 设置权限
RUN chown -R jenkins:jenkins $ANDROID_HOME

# 切换回jenkins用户
USER jenkins

# 设置工作目录
WORKDIR /var/jenkins_home 
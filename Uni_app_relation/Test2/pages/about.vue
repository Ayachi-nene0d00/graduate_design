<template>
<view class="about-page">
  <view class="about-logo">
    <image src="/static/logo.png" class="logo-img" mode="aspectFit" />
  </view>
  <view class="about-title">懂鸟</view>
  <view class="about-version">v1.00</view>
  <button class="about-update-btn" @click="checkUpdate">检查更新</button>
</view>
</template>
<script>
export default {
  methods: {
    checkUpdate() {
      uni.showToast({ title: '当前是最新版本', icon: 'none' });
    }
  }
}
</script>
<style scoped>
.about-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background: #fff;
}
.about-logo {
  margin-top: 80rpx;
  margin-bottom: 40rpx;
}
.logo-img {
  width: 180rpx;
  height: 180rpx;
  border-radius: 90rpx;
  background: #f5f5f5;
}
.about-title {
  font-size: 44rpx;
  font-weight: bold;
  margin-top: 24rpx;
  margin-bottom: 12rpx;
}
.about-version {
  font-size: 28rpx;
  color: #888;
  margin-bottom: 80rpx;
}
.about-update-btn {
  width: 80vw;
  margin-top: auto;
  margin-bottom: 80rpx;
  background: #1aad19;
  color: #fff;
  font-size: 32rpx;
  border-radius: 40rpx;
  height: 80rpx;
  line-height: 80rpx;
}
</style>


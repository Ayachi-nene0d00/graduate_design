<template>
  <view class="terms-page">
    <view class="terms-header">
      <text class="terms-title">使用条款</text>
    </view>
    <scroll-view scroll-y class="terms-scroll">
      <view class="terms-container">
        <view class="policy-title">一、使用条款</view>
        <view class="policy-paragraph">
          欢迎使用uniapp YOLOv8鸟类识别软件（以下简称“本软件”）。本使用条款（以下简称“条款”）是您（用户）与本软件开发者（以下简称“开发者”）之间就使用本软件所订立的具有法律效力的协议。请您在下载、安装、使用本软件前，仔细阅读并充分理解本条款全部内容，一旦您开始使用本软件，即视为您已接受本条款的全部约定，若您不同意本条款任何内容，请立即停止下载、安装和使用本软件。
        </view>
        <view class="policy-section">
          <view class="section-title">1. 软件使用许可</view>
          <view class="section-item">1.1 开发者授予您一项非独占、不可转让、非商业性的免费使用许可，允许您在符合本条款约定的前提下，在个人合法拥有的移动设备上安装、运行本软件，用于个人学习、科研、非商业性鸟类识别及相关公益用途。</view>
          <view class="section-item">1.2 您不得将本软件用于商业用途，包括但不限于利用本软件进行收费识别服务、批量获取鸟类数据用于商业开发、捆绑其他商业软件进行分发等，若需商业使用，需提前与开发者取得联系，获得书面授权并签订相关协议。</view>
          <view class="section-item">1.3 本软件基于YOLOv8算法开发，使用本软件需遵守YOLOv8相关开源协议（AGPL-3.0 license），不得违反协议约定进行修改、分发或商业化使用，若您未遵守该开源协议，开发者有权终止您的使用权限，并追究您的相关责任。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">2. 用户权利与义务</view>
          <view class="section-item">2.1 您有权使用本软件提供的鸟类识别功能，包括拍摄鸟类照片、上传本地鸟类图片进行识别，查看识别结果（鸟类名称、物种简介等），以及使用软件提供的鸟类知识库查询功能。</view>
          <view class="section-item">2.2 您应保证使用本软件时遵守国家法律法规、社会公序良俗，不得利用本软件从事任何违法违规行为，包括但不限于上传虚假、低俗、违法的图片，利用识别结果进行虚假宣传、侵权等活动。</view>
          <view class="section-item">2.3 您应妥善保管自己的设备及软件使用权限，不得将设备转借他人用于违反本条款的用途，若因您自身操作不当、设备丢失或转借他人导致的任何损失，由您自行承担。</view>
          <view class="section-item">2.4 您在使用本软件过程中，应积极配合开发者的版本更新、功能优化，若您拒绝更新软件，可能导致部分功能无法正常使用，开发者不承担相关责任。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">3. 软件限制与免责</view>
          <view class="section-item">3.1 本软件的识别精度受图片清晰度、拍摄角度、环境光线等因素影响，开发者不保证识别结果的100%准确性，仅供参考，不得作为科研、学术研究的唯一依据。</view>
          <view class="section-item">3.2 开发者有权根据技术升级、法律法规要求，对本软件的功能、界面、条款进行修改和更新，更新后的条款将在软件内公示，您继续使用软件即视为接受更新后的条款。</view>
          <view class="section-item">3.3 因不可抗力（包括但不限于地震、洪水、网络中断、设备故障等）、第三方服务异常、您自身操作失误等原因导致本软件无法正常使用或您遭受损失的，开发者不承担任何赔偿责任。</view>
          <view class="section-item">3.4 您不得对本软件进行反向工程、反编译、破解、修改，不得提取软件中的算法、代码、数据等核心内容，若违反本条约定，开发者有权追究您的侵权责任，要求您赔偿全部损失。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">4. 条款终止</view>
          <view class="section-item">4.1 若您违反本条款任何约定，开发者有权立即终止您的使用权限，收回软件使用许可，且不承担任何补偿责任。</view>
          <view class="section-item">4.2 您可随时停止使用本软件，停止使用后，本条款自动终止，但您仍需遵守本条款中关于知识产权、保密等相关约定。</view>
          <view class="section-item">4.3 开发者有权根据自身发展需要，终止本软件的运营、维护，终止前将在软件内提前7天公示，公示期满后，本软件将停止提供服务，条款自动终止，开发者不承担任何赔偿责任。</view>
        </view>
      </view>
    </scroll-view>
    <view class="terms-footer">
      <button class="read-btn" @click="onRead">已阅读</button>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    onRead() {
      uni.navigateBack();
    }
  }
}
</script>

<style scoped>
.terms-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #fff;
}
.terms-header {
  display: flex;
  align-items: center;
  height: 100rpx;
  border-bottom: 1rpx solid #eee;
  background: #fff;
  padding: 0 32rpx;
}
.terms-title {
  font-size: 36rpx;
  font-weight: bold;
  flex: 1;
  text-align: center;
  color: #222;
}
.terms-scroll {
  flex: 1;
  width: 100%;
  background: #fff;
}
.terms-container {
  padding: 32rpx 40rpx 0;
  background-color: #fff;
  border-radius: 16rpx;
}
.policy-title {
  font-size: 40rpx;
  font-weight: bold;
  text-align: center;
  margin-bottom: 32rpx;
  color: #1A1A1A;
}
.policy-paragraph {
  font-size: 28rpx;
  line-height: 1.6;
  color: #333;
  margin-bottom: 32rpx;
  text-align: justify;
}
.policy-section {
  margin-bottom: 32rpx;
}
.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2C3E50;
  margin-bottom: 20rpx;
  border-left: 6rpx solid #4CAF50;
  padding-left: 20rpx;
}
.section-item {
  font-size: 28rpx;
  line-height: 1.6;
  color: #333;
  margin-bottom: 16rpx;
  text-align: justify;
}
.section-item:last-child {
  margin-bottom: 0;
}
.terms-footer {
  width: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32rpx 0 32rpx 0;
  position: sticky;
  bottom: 0;
  z-index: 10;
}
.read-btn {
  width: 80vw;
  max-width: 600rpx;
  background: #4CAF50;
  color: #fff;
  border-radius: 48rpx;
  font-size: 32rpx;
  font-weight: bold;
  padding: 20rpx 0;
  margin: 0 auto;
  box-shadow: 0 4rpx 16rpx rgba(76,175,80,0.08);
}
</style>

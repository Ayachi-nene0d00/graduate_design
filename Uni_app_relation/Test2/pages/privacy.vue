<template>
  <view class="privacy-page">
    <view class="privacy-header">
      <text class="privacy-title">隐私政策</text>
    </view>
    <scroll-view scroll-y class="privacy-scroll">
      <view class="privacy-container">
        <view class="policy-title">二、隐私政策</view>
        <view class="policy-paragraph">
          本隐私政策旨在向您说明，在使用uniapp YOLOv8鸟类识别软件（以下简称“本软件”）过程中，我们如何收集、使用、存储、保护您的个人信息及相关数据，以及您享有的相关权利。本政策遵循《中华人民共和国个人信息保护法》《网络数据安全管理条例》等相关法律法规要求，切实保护您的隐私权益。请您仔细阅读本政策，若您使用本软件，即视为您同意我们按照本政策处理您的相关信息。
        </view>

        <view class="policy-section">
          <view class="section-title">1. 信息收集范围</view>
          <view class="section-item">1.1 必要信息：为实现软件核心功能（鸟类识别），我们会收集您使用软件时上传或拍摄的鸟类图片数据。该数据仅用于识别分析，不会包含您的个人身份信息、人脸信息等敏感内容，且不会用于识别、关联任何自然人身份。</view>
          <view class="section-item">1.2 设备相关信息：为保障软件正常运行、优化软件性能，我们会自动收集您的设备基础信息，包括设备型号、操作系统版本、设备唯一标识符、网络连接状态。该类信息不涉及您的个人隐私，仅用于技术维护和功能优化。</view>
          <view class="section-item">1.3 自愿信息：您可选择是否提供姓名、联系方式、兴趣爱好等个人信息，该类信息仅用于为您提供个性化服务（如鸟类观测提醒、知识库推送等）。若您不提供，不影响软件核心功能的使用。</view>
          <view class="section-item">1.4 不收集信息：我们不会收集您的人脸信息、地理位置信息、通讯录、短信、通话记录、银行账户信息等敏感个人信息，也不会通过任何方式窃取、获取您的其他私人信息。</view>
        </view>

        <view class="policy-section">
          <view class="section-title">2. 信息使用方式</view>
          <view class="section-item">2.1 核心用途：收集的鸟类图片数据仅用于YOLOv8算法的识别分析，生成识别结果（鸟类名称、物种简介等）并展示给您。识别完成后，原始图片数据仅存储在您的本地设备，不会上传至我们的服务器（除非您主动选择上传至云端备份）。</view>
          <view class="section-item">2.2 优化用途：我们会对匿名化处理后的识别数据（去除所有可识别信息，仅保留鸟类特征数据）进行汇总分析，用于优化算法精度、完善鸟类知识库，提升软件识别效果。该过程中不会涉及任何您的个人信息。</view>
          <view class="section-item">2.3 服务用途：若您提供了自愿信息，我们会根据您的需求，为您推送相关鸟类资讯、观测提醒等服务。您可随时取消订阅，停止接收相关推送。</view>
          <view class="section-item">2.4 合规用途：在法律法规要求、司法机关调查取证或维护软件安全、用户合法权益的情况下，我们可能会依法使用相关信息，且会严格遵循最小必要原则，仅提供必要的信息。</view>
        </view>

        <view class="policy-section">
          <view class="section-title">3. 信息存储与保护</view>
          <view class="section-item">3.1 存储方式：您上传或拍摄的原始图片数据，默认仅存储在您的本地设备，不会上传至我们的服务器。若您选择云端备份，数据将加密存储在我们的安全服务器，采用数据加密、访问控制、入侵检测和防御等措施保障数据安全，符合相关信息安全规范。</view>
          <view class="section-item">3.2 存储期限：本地存储的数据由您自行管理，可随时删除。云端备份的数据，您可随时手动删除。若您连续12个月未使用本软件，我们将自动删除您的云端备份数据，确保数据不会被长期留存。</view>
          <view class="section-item">3.3 保护措施：我们建立了完善的信息安全保护体系，采用加密技术、安全审计、权限管理等措施，防止信息被泄露、篡改、丢失、非法获取或使用。我们仅授权必要的技术人员访问相关数据，且对技术人员进行严格的保密培训，明确保密责任。</view>
          <view class="section-item">3.4 第三方合作：我们不会将您的任何个人信息、图片数据泄露给第三方，除非获得您的明确同意，或法律法规另有规定。若因第三方服务（如云端存储服务商）导致信息泄露，我们将协助您追究第三方的责任，但不承担直接赔偿责任。</view>
        </view>

        <view class="policy-section">
          <view class="section-title">4. 用户权利</view>
          <view class="section-item">4.1 查看与删除权：您可随时查看本地存储的图片数据、设备相关信息，可手动删除本地图片、取消云端备份，也可联系我们删除您提供的自愿信息。我们将在收到您的请求后3个工作日内完成处理。</view>
          <view class="section-item">4.2 撤回同意权：您可随时撤回对信息收集、使用的同意。撤回同意后，我们将停止收集、使用您的相关信息，但不影响撤回前基于您的同意已进行的信息处理活动的效力，也不影响软件核心功能的正常使用。</view>
          <view class="section-item">4.3 投诉与咨询权：若您对信息处理有任何疑问、异议，或认为您的隐私权益受到侵害，可联系我们的客服。我们将在3个工作日内给予您回复，并妥善处理您的问题。</view>
        </view>

        <view class="policy-section">
          <view class="section-title">5. 政策更新</view>
          <view class="section-item">我们会根据法律法规的更新、软件功能的优化，对本隐私政策进行修改和完善。更新后的政策将在软件内公示，您继续使用软件即视为接受更新后的隐私政策。若您不同意更新后的政策，请立即停止使用本软件。</view>
        </view>
      </view>
    </scroll-view>
    <view class="privacy-footer">
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
.privacy-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #fff;
}
.privacy-header {
  display: flex;
  align-items: center;
  height: 100rpx;
  border-bottom: 1rpx solid #eee;
  background: #fff;
  padding: 0 32rpx;
}
.privacy-title {
  font-size: 36rpx;
  font-weight: bold;
  flex: 1;
  text-align: center;
  color: #222;
}
.privacy-scroll {
  flex: 1;
  width: 100%;
  background: #fff;
}
.privacy-container {
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
.privacy-footer {
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

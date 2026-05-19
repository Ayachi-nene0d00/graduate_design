<template>
  <view class="copyright-page">
    <view class="copyright-header">
      <text class="copyright-title">版权声明</text>
    </view>
    <scroll-view scroll-y class="copyright-scroll">
      <view class="copyright-container">
        <view class="policy-title">三、版权声明</view>
        <view class="policy-paragraph">
          本声明旨在明确uniapp YOLOv8鸟类识别软件（以下简称“本软件”）的知识产权归属及使用限制，保护开发者及相关权利人的合法权益，您使用本软件即视为您遵守本版权声明的全部约定。
        </view>
        <view class="policy-section">
          <view class="section-title">1. 软件知识产权归属</view>
          <view class="section-item">1.1 本软件的整体著作权（包括但不限于软件代码、界面设计、图标、文字说明、功能逻辑等）均归本软件开发者所有，受《中华人民共和国著作权法》《计算机软件保护条例》等相关法律法规保护，开发者享有完整的著作权。</view>
          <view class="section-item">1.2 本软件基于YOLOv8算法开发，YOLOv8算法及相关模型的版权归Ultralytics公司所有，使用本软件需严格遵守YOLOv8相关开源协议（AGPL-3.0 license），不得违反协议约定进行修改、分发、商业化使用或其他侵权行为。若您未遵守该开源协议，需自行承担相应的法律责任，与本软件开发者无关。</view>
          <view class="section-item">1.3 本软件中包含的鸟类知识库、图片素材、物种简介等内容，若涉及第三方版权，均已获得相关权利人的授权，仅供用户在使用软件时参考，不得单独提取、复制、传播或用于其他用途，否则将构成侵权。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">2. 版权使用限制</view>
          <view class="section-item">2.1 您仅有权在本使用条款约定的范围内，使用本软件的功能，不得复制、修改、传播、出租、出售、分销本软件的任何部分，不得对软件进行反向工程、反编译、破解，不得提取软件中的核心代码、算法、数据等内容。</view>
          <view class="section-item">2.2 您不得将本软件的识别结果、鸟类知识库内容用于商业用途，不得擅自转载、传播、篡改相关内容，若需用于科研、学术、公益等非商业用途，需注明来源（uniapp YOLOv8鸟类识别软件），且不得侵犯相关权利人的版权。</view>
          <view class="section-item">2.3 您不得利用本软件制作、传播侵犯第三方版权的内容，不得使用本软件侵犯他人的知识产权、肖像权、名誉权等合法权益，若因您的行为导致第三方投诉、索赔或开发者遭受损失，由您承担全部责任。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">3. 侵权责任</view>
          <view class="section-item">3.1 若您违反本版权声明，侵犯本软件开发者或第三方的知识产权，开发者有权立即终止您的使用权限，要求您停止侵权行为、删除侵权内容，并赔偿开发者及第三方的全部损失（包括但不限于律师费、诉讼费、误工费等）。</view>
          <view class="section-item">3.2 若您发现本软件存在侵犯第三方版权的内容，或他人利用本软件进行侵权行为，请及时联系我们，我们将在收到通知后3个工作日内核实处理，立即删除侵权内容，并追究相关人员的责任。</view>
        </view>
        <view class="policy-section">
          <view class="section-title">4. 其他说明</view>
          <view class="section-item">本版权声明自本软件发布之日起生效，随软件版本更新同步调整，更新后的声明将在软件内公示，您继续使用软件即视为接受更新后的版权声明。</view>
          <view class="section-item">本软件开发者保留对本版权声明的最终解释权，若您对本声明有任何疑问，可联系我们咨询。</view>
        </view>
      </view>
    </scroll-view>
    <view class="copyright-footer">
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
.copyright-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #fff;
}
.copyright-header {
  display: flex;
  align-items: center;
  height: 100rpx;
  border-bottom: 1rpx solid #eee;
  background: #fff;
  padding: 0 32rpx;
}
.copyright-title {
  font-size: 36rpx;
  font-weight: bold;
  flex: 1;
  text-align: center;
  color: #222;
}
.copyright-scroll {
  flex: 1;
  width: 100%;
  background: #fff;
}
.copyright-container {
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
.copyright-footer {
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

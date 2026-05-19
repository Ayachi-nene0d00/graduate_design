<!-- login.vue: 登录页面，提供微信一键登录或跳过登录选项 -->
<template>
	<view class="login-page">
								<image src="../static/logo.png" class="logo" mode="aspectFit" />
		<view class="desc">AI 鸟类识别系统</view>
		<button class="wechat-login-btn" @click="onWeChatLogin">
			<image src="/static/wechat.png" class="wechat-icon" />
			微信一键登录
		</button>
		<!-- 跳过登录按钮始终可点，不用 :disabled -->
		<button class="skip-login-btn" @click="onSkipLogin">跳过登录</button>
		<view class="agreement-row" @click="toggleAgree">
			<text class="checkmark" :class="{checked: agreed}">{{ agreed ? '✔' : '' }}</text>
			<text>我已阅读并同意</text>
			<text class="link" @click.stop="goToTerms">《使用条款》</text>
			<text>和</text>
			<text class="link" @click.stop="goToPrivacy">《隐私政策须知》</text>
		</view>
	</view>
</template>

<script>
// 脚本部分：处理微信登录和跳过登录的逻辑
export default {
  data() {
    return {
      agreed: false
    };
  },
  methods: {
    onWeChatLogin() {
      if (!this.agreed) {
        uni.showToast({
          title: '请先阅读并同意使用条款和隐私政策',
          icon: 'none'
        });
        return;
      }
      // #ifdef APP-PLUS
      uni.login({
        provider: 'weixin',
        success: (loginRes) => {
          uni.getUserInfo({
            provider: 'weixin',
            success: (infoRes) => {
              uni.setStorageSync('user_info', infoRes.userInfo);
              uni.reLaunch({ url: '/pages/index/index' });
            }
          });
        }
      });
      // #endif
    },
    onSkipLogin() {
      if (!this.agreed) {
        uni.showToast({
          title: '请先阅读并同意使用条款和隐私政策',
          icon: 'none'
        });
        return;
      }
      uni.reLaunch({ url: '/pages/index/index' });
    },
    toggleAgree() {
      this.agreed = !this.agreed;
    },
    goToTerms() {
      uni.navigateTo({ url: '/pages/terms' });
    },
    goToPrivacy() {
      uni.navigateTo({ url: '/pages/privacy' });
    }
  }
};
</script>

<style scoped>
/* 样式部分：登录页面的布局和样式 */
.login-page {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	height: 100vh;
	background: #f8f8f8;
}
.logo {
	width: 120px;
	height: 120px;
	margin-bottom: 32px;
}
.desc {
	font-size: 22px;
	margin-bottom: 40px;
	color: #333;
}
.wechat-login-btn {
	display: flex;
	align-items: center;
	background: #1aad19;
	color: #fff;
	font-size: 18px;
	padding: 12px 32px;
	border-radius: 24px;
}
.wechat-icon {
	width: 28px;
	height: 28px;
	margin-right: 12px;
}
.skip-login-btn {
  margin-top: 24rpx;
  width: 60vw;
  max-width: 400rpx;
  background: #fff;
  color: #1aad19;
  border: 1px solid #1aad19;
  border-radius: 16rpx;
  font-size: 30rpx;
  padding: 18rpx 0;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  display: block;
}
.agreement-row {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 32rpx;
  font-size: 28rpx;
  color: #222;
  user-select: none;
}
.checkmark {
  color: #bbb;
  font-size: 32rpx;
  margin-right: 8rpx;
  border: 1px solid #bbb;
  border-radius: 50%;
  width: 36rpx;
  height: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  margin-left: 0;
  margin-top: 0;
  margin-bottom: 0;
  margin-right: 8rpx;
}
.checkmark.checked {
  color: #4CAF50;
  border-color: #4CAF50;
  background: #e8f5e9;
}
.link {
  color: #4CAF50;
  margin: 0 4rpx;
  text-decoration: underline;
}
</style>

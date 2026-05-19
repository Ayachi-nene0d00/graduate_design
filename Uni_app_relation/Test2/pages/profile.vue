<template>
	<view class="profile-page">
		<!-- 头部背景区域 -->
		<view class="header-bg"></view>

		<!-- 用户信息区域（已登录/未登录统一布局） -->
		<view class="user-section">
			<view class="user-info merged-info">
				<image :src="user.nickName ? user.avatarUrl : '/image/logo/guest_avatar.png'" class="avatar" mode="aspectFill" />
				<view class="user-text">
					<view class="nickname">{{ user.nickName ? user.nickName : '未登录' }}</view>
				</view>
				<button v-if="!user.nickName" class="wechat-login-btn" @click="goToLogin">微信登录</button>
			</view>
		</view>

		<!-- 功能菜单列表：始终显示 -->
		<view class="menu-list">
			<!-- 分组：其他 -->
			<view class="menu-group-header">其他</view>

			<!-- 存储空间 -->
			<view class="menu-item" @click="goToStorage">
				<view class="menu-left">
					<text class="menu-icon">💾</text>
					<text class="menu-label">存储空间</text>
				</view>
				<text class="menu-arrow">›</text>
			</view>

			<!-- 使用条款 -->
			<view class="menu-item" @click="goToTerms">
				<view class="menu-left">
					<text class="menu-icon">📜</text>
					<text class="menu-label">使用条款</text>
				</view>
				<text class="menu-arrow">›</text>
			</view>

			<!-- 隐私政策 -->
			<view class="menu-item" @click="goToPrivacy">
				<view class="menu-left">
					<text class="menu-icon">🔒</text>
					<text class="menu-label">隐私政策</text>
				</view>
				<text class="menu-arrow">›</text>
			</view>

			<!-- 版权声明 -->
			<view class="menu-item" @click="goToCopyright">
				<view class="menu-left">
					<text class="menu-icon">©️</text>
					<text class="menu-label">版权声明</text>
				</view>
				<text class="menu-arrow">›</text>
			</view>

			<!-- 关于 -->
			<view class="menu-item" @click="goToAbout">
				<view class="menu-left">
					<text class="menu-icon">ℹ️</text>
					<text class="menu-label">关于</text>
				</view>
				<text class="menu-arrow">›</text>
			</view>
		</view>

		<!-- 操作按钮区域 - 竖直排列圆角按钮 -->
		<view class="action-buttons-vertical">
			<button class="action-btn vertical" @click="clearHistory">
				<text class="iconfont">🗑️</text> 清空识别/搜索历史
			</button>
			<button class="action-btn vertical" @click="goToServerConfig">
				<text class="iconfont">⚙️</text> 服务地址配置
			</button>
			<button v-if="user.nickName" class="action-btn vertical logout" @click="logout">
				<text class="iconfont">⎋</text> 退出登录
			</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			user: {
				avatarUrl: '',
				nickName: ''
			},
			showPinyin: false,
			showLatinName: false
		};
	},
	onShow() {
		const info = uni.getStorageSync('user_info') || {};
		this.user = info;
		// 加载设置
		this.showPinyin = uni.getStorageSync('show_pinyin') || false;
		this.showLatinName = uni.getStorageSync('show_latin') || false;
	},
	methods: {
		clearHistory() {
			uni.showModal({
				title: '提示',
				content: '确定清空所有历史记录？',
				success: (res) => {
					if (res.confirm) {
						uni.removeStorageSync('bird_history');
						uni.removeStorageSync('search_history');
						uni.showToast({ title: '已清空' });
					}
				}
			});
		},
		logout() {
			uni.showModal({
				title: '提示',
				content: '确定退出登录？',
				success: (res) => {
					if (res.confirm) {
						uni.removeStorageSync('user_info');
						this.user = {};
						uni.showToast({ title: '已退出' });
					}
				}
			});
		},
		goToLogin() {
			uni.navigateTo({ url: '/pages/login' });
		},
		goToServerConfig() {
			uni.navigateTo({ url: '/pages/server_config' });
		},
		togglePinyin(e) {
			this.showPinyin = e.detail.value;
			uni.setStorageSync('show_pinyin', this.showPinyin);
		},
		toggleLatinName(e) {
			this.showLatinName = e.detail.value;
			uni.setStorageSync('show_latin', this.showLatinName);
		},
		goToBitrate() {
			uni.showToast({ title: 'MP3比特率设置开发中', icon: 'none' });
		},
		goToSampleRate() {
			uni.showToast({ title: '采样率设置开发中', icon: 'none' });
		},
		goToStorage() {
			uni.showActionSheet({
				itemList: ['清除缓存', '清除数据'],
				success: (res) => {
					if (res.tapIndex === 0) {
						// 清除缓存
						uni.clearStorageSync();
						uni.showToast({ title: '缓存已清除' });
					} else if (res.tapIndex === 1) {
						// 清除数据
						uni.clearStorageSync();
						// 可扩展：如有本地数据库/文件等，需一并清理
						uni.showToast({ title: '数据已清除' });
					}
				}
			});
		},
		goToAnnouncement() {
			uni.showToast({ title: '公告页面开发中', icon: 'none' });
		},
		goToFeedback() {
			uni.showToast({ title: '反馈页面开发中', icon: 'none' });
		},
		goToTerms() {
			uni.navigateTo({ url: '/pages/terms' });
		},
		goToPrivacy() {
			uni.navigateTo({ url: '/pages/privacy' });
		},
		goToCopyright() {
			uni.navigateTo({ url: '/pages/copyright' });
		},
		goToAbout() {
			uni.navigateTo({ url: '/pages/about' });
		},
	}
};
</script>

<style scoped>
.profile-page {
	min-height: 100vh;
	background-color: #f5f5f5;
	position: relative;
}

/* 头部背景 */
.header-bg {
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	height: 200rpx;
	background: linear-gradient(135deg, #2c7da0 0%, #1f5068 100%);
	border-radius: 0 0 30rpx 30rpx;
}

/* 用户信息区域 */
.user-section {
	padding: 40rpx 32rpx 0;
	position: relative;
	z-index: 2;
}

.user-info {
	display: flex;
	align-items: center;
	gap: 24rpx;
	background: #fff;
	padding: 32rpx;
	border-radius: 24rpx;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.merged-info {
	gap: 20rpx;
	width: 100%;
	justify-content: flex-start;
}

.avatar {
	width: 120rpx;
	height: 120rpx;
	border-radius: 60rpx;
	border: 3rpx solid #fff;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
}

.user-text {
	flex: 1;
}

.nickname {
	font-size: 36rpx;
	font-weight: 600;
	color: #1a1a1a;
}

/* 菜单列表 */
.menu-list {
	margin: 24rpx 32rpx 32rpx;
	background: #fff;
	border-radius: 24rpx;
	overflow: hidden;
	position: relative;
	z-index: 2;
}

.menu-group-header {
	padding: 24rpx 32rpx 12rpx;
	font-size: 26rpx;
	color: #999;
	background: #fff;
	font-weight: 500;
}

.menu-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 28rpx 32rpx;
	background: #fff;
	border-bottom: 1rpx solid #f5f5f5;
	transition: background 0.2s;
}

.menu-item:active {
	background: #fafafa;
}

.menu-left {
	display: flex;
	align-items: center;
	gap: 20rpx;
}

.menu-icon {
	font-size: 40rpx;
	width: 48rpx;
}

.menu-label {
	font-size: 30rpx;
	color: #1a1a1a;
}

.menu-right {
	display: flex;
	align-items: center;
	gap: 16rpx;
}

.menu-value {
	font-size: 28rpx;
	color: #999;
}

.menu-arrow {
	font-size: 36rpx;
	color: #ccc;
}

/* 操作按钮区域 - 左右边距2px */
.action-buttons {
	margin: 32rpx 2px 40rpx;
	display: flex;
	flex-direction: column;
	gap: 20rpx;
	position: relative;
	z-index: 2;
}

.action-buttons-full {
	display: none;
}
.action-buttons-vertical {
	display: flex;
	flex-direction: column;
	gap: 24rpx;
	margin: 32rpx 32rpx 40rpx 32rpx;
}
.action-btn {
	background: #fff;
	color: #333;
	font-size: 30rpx;
	padding: 24rpx 0;
	border-radius: 16rpx;
	border: none;
	box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.03);
	font-weight: 500;
}

.action-btn::after {
	border: none;
}

.logout {
	background: #ff4d4f;
	color: #fff;
}

.action-btn.vertical {
	width: 100%;
	border-radius: 32rpx;
	font-size: 32rpx;
	padding: 28rpx 0;
	display: flex;
	align-items: center;
	justify-content: center;
	background: #fff;
	color: #e54d42;
	font-weight: 500;
	box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.03);
	border: none;
}
.action-btn.vertical .iconfont {
	margin-right: 16rpx;
	font-size: 36rpx;
}
.action-btn.vertical.logout {
	background: #fff;
	color: #e54d42;
	border: 2rpx solid #e54d42;
}

/* 登录提示 */
.login-prompt {
	display: flex;
	justify-content: center;
	align-items: center;
	min-height: 60vh;
}

.wechat-login-btn {
	background: #1aad19;
	color: #fff;
	font-size: 28rpx;
	padding: 0 32rpx;
	height: 60rpx;
	line-height: 60rpx;
	border-radius: 40rpx;
	border: none;
	margin-left: auto;
	box-shadow: 0 4rpx 10rpx rgba(26, 173, 25, 0.25);
	display: flex;
	align-items: center;
}

.wechat-login-btn::after {
	border: none;
}
</style>
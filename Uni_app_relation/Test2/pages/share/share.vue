<!-- share.vue: 分享页面，展示识别结果的海报，提供分享、百科搜索和返回功能 -->
<template>
	<view class="share-page">
		<view class="poster-card">
			<image :src="birdImg" mode="aspectFill" class="bird-hero"></image>
			<view class="poster-body">
				<view class="result-header">
					<text class="bird-name">{{ birdName }}</text>
					<view class="conf-tag">匹配度 {{ (confidence * 100).toFixed(1) }}%</view>
				</view>
				<view class="divider"></view>
				<view class="footer-info">
					<text class="info-item">识别来源：AI 离线引擎</text>
					<text class="info-item">技术支持：西安建筑科技大学 · 王全宝</text>
				</view>
			</view>
		</view>

		<view class="action-section">
			<button class="btn-share" @click="handleSystemShare">
				<text class="icon">↗</text> 立即分享给好友
			</button>
			
			<view class="btn-row">
				<view class="sub-btn" @click="goWiki">
					<text>📖 鸟类百科</text>
				</view>
				<view class="sub-btn" @click="goSearch">
					<text>🔍 深度搜索</text>
				</view>
			</view>
			
			<button class="btn-back" @click="goBack">返回首页</button>
		</view>
	</view>
</template>

<script>
// 脚本部分：处理分享、跳转到百科和搜索的逻辑
import { requestApi } from '@/common/api';
import { localizeBirdName } from '@/common/bird_name_localizer';

export default {
	data() {
		return {
			birdName: '',
			birdImg: '',
			confidence: 0
		};
	},
	async onLoad(options) {
		// 接收首页传来的参数
		this.birdName = await localizeBirdName(options.name || '', requestApi);
		this.birdImg = decodeURIComponent(options.img);
		this.confidence = parseFloat(options.conf || 0);
	},
	methods: {
		handleSystemShare() {
			const shareText = `我刚才识别出一只【${this.birdName}】，AI匹配度高达${(this.confidence*100).toFixed(1)}%！`;
			// #ifdef APP-PLUS
			uni.shareWithSystem({
				summary: shareText,
				href: 'http://www.birdnet.cn/',
				success: () => { uni.showToast({ title: '分享成功' }); }
			});
			// #endif
			// #ifdef H5
			uni.setClipboardData({
				data: shareText,
				success: () => { uni.showToast({ title: '结果已复制，请粘贴发送', icon: 'none' }); }
			});
			// #endif
		},
		goWiki() {
			uni.navigateTo({
				url: `/pages/webview/webview?url=${encodeURIComponent('http://www.birdnet.cn/')}`
			});
		},
		goSearch() {
			const searchUrl = `https://www.bing.com/search?q=${encodeURIComponent(this.birdName)}`;
			uni.navigateTo({
				url: `/pages/webview/webview?url=${encodeURIComponent(searchUrl)}`
			});
		},
		goBack() {
			uni.navigateBack();
		}
	}
}
</script>

<style scoped>
/* 样式部分：分享页面的布局和样式 */
.share-page { padding: 40rpx; background: #f0f2f5; min-height: 100vh; }
.poster-card { background: #fff; border-radius: 40rpx; overflow: hidden; box-shadow: 0 20rpx 40rpx rgba(0,0,0,0.08); }
.bird-hero { width: 100%; height: 650rpx; background: #eee; }
.poster-body { padding: 40rpx; }
.result-header { display: flex; justify-content: space-between; align-items: center; }
.bird-name { font-size: 44rpx; font-weight: bold; color: #2d3436; flex: 1; }
.conf-tag { background: #e1f5fe; color: #03a9f4; padding: 8rpx 20rpx; border-radius: 12rpx; font-size: 24rpx; font-weight: bold; }
.divider { height: 2rpx; background: #f1f2f6; margin: 30rpx 0; }
.footer-info { display: flex; flex-direction: column; gap: 10rpx; }
.info-item { font-size: 22rpx; color: #b2bec3; }

.action-section { margin-top: 50rpx; }
.btn-share { background: #00b894; color: #fff; border-radius: 50rpx; height: 100rpx; line-height: 100rpx; font-weight: bold; box-shadow: 0 10rpx 20rpx rgba(0,184,148,0.2); }
.btn-row { display: flex; gap: 20rpx; margin-top: 30rpx; }
.sub-btn { flex: 1; background: #fff; height: 90rpx; display: flex; justify-content: center; align-items: center; border-radius: 20rpx; font-size: 28rpx; color: #636e72; }
.btn-back { margin-top: 40rpx; background: transparent; color: #b2bec3; font-size: 26rpx; border: none; }
.btn-back::after { border: none; }
</style>

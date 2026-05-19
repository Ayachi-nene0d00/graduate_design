<!-- server_config.vue: 后端服务地址配置页面，支持扫码和手动输入 -->
<template>
	<view class="config-page">
		<view class="header">
			<text class="title">服务连接配置</text>
			<text class="subtitle">扫码或手动输入后端地址</text>
		</view>
		<view class="form">
			<text class="label">当前地址</text>
			<view class="current">{{ currentBaseUrl }}</view>
			<text class="label">新地址</text>
			<input v-model="inputUrl" class="input" placeholder="例如: http://192.168.1.10:8000" />
			<view class="btn-row">
				<button class="btn" @click="save">保存</button>
				<button class="btn secondary" @click="scan">扫码</button>
			</view>
		</view>
	</view>
</template>

<script>
import { getBaseUrl, setBaseUrl } from '@/common/api';

export default {
	data() {
		return {
			currentBaseUrl: getBaseUrl(),
			inputUrl: ''
		};
	},
	methods: {
		save() {
			if (!this.inputUrl.trim()) {
				uni.showToast({ title: '请输入地址', icon: 'none' });
				return;
			}
			this.currentBaseUrl = setBaseUrl(this.inputUrl.trim());
			uni.showToast({ title: '已保存', icon: 'success' });
		},
		scan() {
			// #ifdef APP-PLUS
			uni.scanCode({
				success: (res) => {
					const scanned = (res.result || '').trim();
					if (scanned.startsWith('http')) {
						this.inputUrl = scanned;
						this.currentBaseUrl = setBaseUrl(scanned);
						uni.showToast({ title: '扫码成功', icon: 'success' });
					} else {
						uni.showToast({ title: '二维码内容无效', icon: 'none' });
					}
				},
				fail: () => {
					uni.showToast({ title: '扫码失败', icon: 'none' });
				}
			});
			// #endif
			// #ifndef APP-PLUS
			uni.showToast({ title: '当前平台不支持扫码', icon: 'none' });
			// #endif
		}
	}
};
</script>

<style scoped>
.config-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 32rpx; }
.title { font-size: 36rpx; font-weight: bold; color: #2d3436; display: block; }
.subtitle { font-size: 24rpx; color: #636e72; margin-top: 8rpx; display: block; }
.form { background: #fff; padding: 24rpx; border-radius: 16rpx; box-shadow: 0 6rpx 16rpx rgba(0,0,0,0.06); }
.label { font-size: 24rpx; color: #636e72; margin-bottom: 8rpx; display: block; }
.current { font-size: 26rpx; color: #2d3436; margin-bottom: 16rpx; }
.input { border: 1px solid #e0e0e0; border-radius: 12rpx; padding: 16rpx; font-size: 26rpx; margin-bottom: 16rpx; }
.btn-row { display: flex; gap: 16rpx; }
.btn { flex: 1; background: #0984e3; color: #fff; border-radius: 12rpx; font-size: 26rpx; padding: 10rpx 0; }
.btn.secondary { background: #00b894; }
</style>


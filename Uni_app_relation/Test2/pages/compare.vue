<!-- compare.vue: 鸟类对比页面，用户可以选择两只鸟类进行对比，显示名称、习性、保护级别等信息 -->
<template>
	<view class="compare-page">
		<view class="header">
			<text class="title">鸟类对比</text>
		</view>
		<picker mode="selector" :range="birdNames" @change="onPick1">
			<view class="picker">选择鸟类1：{{ bird1 || '未选择' }}</view>
		</picker>
		<picker mode="selector" :range="birdNames" @change="onPick2">
			<view class="picker">选择鸟类2：{{ bird2 || '未选择' }}</view>
		</picker>
		<view v-if="bird1 && bird2" class="compare-result">
			<view class="compare-row">
				<view class="compare-col">
					<image v-if="getBirdImg(bird1)" :src="getBirdImg(bird1)" class="bird-img" mode="aspectFill" @click="previewImg(getBirdImg(bird1))" />
					<text class="compare-label">名称</text>
					<text>{{ bird1 }}</text>
				</view>
				<view class="compare-col">
					<image v-if="getBirdImg(bird2)" :src="getBirdImg(bird2)" class="bird-img" mode="aspectFill" @click="previewImg(getBirdImg(bird2))" />
					<text class="compare-label">名称</text>
					<text>{{ bird2 }}</text>
				</view>
			</view>
			<view class="compare-row">
				<view class="compare-col">
					<text class="compare-label">习性</text>
					<text>{{ getInfo(bird1, 'habit') }}</text>
				</view>
				<view class="compare-col">
					<text class="compare-label">习性</text>
					<text>{{ getInfo(bird2, 'habit') }}</text>
				</view>
			</view>
			<view class="compare-row">
				<view class="compare-col">
					<text class="compare-label">保护级别</text>
					<text>{{ getInfo(bird1, 'protect') }}</text>
				</view>
				<view class="compare-col">
					<text class="compare-label">保护级别</text>
					<text>{{ getInfo(bird2, 'protect') }}</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
// 脚本部分：处理鸟类选择和信息获取逻辑
import { requestApi, getBaseUrl } from '@/common/api';
export default {
	data() {
		return {
			birdNames: [],
			bird1: '',
			bird2: '',
			birds: []
		};
	},
	onLoad() {
		this.loadBirds();
	},
	methods: {
		async loadBirds() {
			try {
				const res = await requestApi({ path: '/api/bird?page=1&page_size=100', method: 'GET' });
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					this.birds = response.data.data;
					this.birdNames = this.birds.map(b => b.name);
				}
			} catch (e) {
				this.birds = [];
				this.birdNames = [];
			}
		},
		onPick1(e) { this.bird1 = this.birdNames[e.detail.value]; },
		onPick2(e) { this.bird2 = this.birdNames[e.detail.value]; },
		getInfo(name, key) {
			const b = this.birds.find(b => b.name === name);
			if (!b) return '暂无数据';
			if (key === 'protect') return b.protect_level || '暂无数据';
			return b[key] ? b[key] : '暂无数据';
		},
		getBirdImg(name) {
			const b = this.birds.find(b => b.name === name);
			if (!b) return '';
			const url = b.image_url || '';
			if (!url) return 'https://img.haoma.com/bird_placeholder.jpg';
			if (url.startsWith('http')) return url;
			return getBaseUrl() + (url.startsWith('/') ? url : '/' + url);
		},
		previewImg(url) {
			if (!url) return;
			uni.previewImage({
				urls: [url],
				current: url
			});
		}
	}
};
</script>

<style scoped>
/* 样式部分：鸟类对比页面的布局和样式 */
.compare-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 24rpx; }
.title { font-size: 40rpx; font-weight: bold; color: #2d3436; }
.picker { background: #f5f5f5; border-radius: 8rpx; padding: 16rpx; margin-bottom: 18rpx; color: #333; }
.compare-result { margin-top: 24rpx; }
.compare-row { display: flex; gap: 18rpx; margin-bottom: 18rpx; }
.compare-col { flex: 1; background: #fff; border-radius: 12rpx; padding: 18rpx; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.03); }
.compare-label { color: #00b894; font-size: 16px; margin-bottom: 8rpx; display: block; }
.bird-img { width: 120rpx; height: 120rpx; border-radius: 12rpx; margin-bottom: 12rpx; background: #f5f5f5; }
</style>

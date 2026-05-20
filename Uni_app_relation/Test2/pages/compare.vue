<!-- compare.vue: 鸟类对比页面，用户可以选择两只鸟类进行对比，显示名称、习性、保护级别等信息 -->
<template>
	<view class="compare-page">
		<view class="header">
			<text class="title">鸟类对比</text>
		</view>
		<view class="search-select">
			<input
				v-model="query1"
				class="search-input"
				placeholder="搜索并选择鸟类1"
				@focus="showOptions1 = true"
				@input="onQueryInput(1)"
			/>
			<scroll-view v-if="showOptions1 && filteredBirds1.length" scroll-y class="options-list">
				<view class="option-item" v-for="name in filteredBirds1" :key="`b1-${name}`" @click="selectBird(1, name)">
					{{ name }}
				</view>
			</scroll-view>
		</view>
		<view class="search-select">
			<input
				v-model="query2"
				class="search-input"
				placeholder="搜索并选择鸟类2"
				@focus="showOptions2 = true"
				@input="onQueryInput(2)"
			/>
			<scroll-view v-if="showOptions2 && filteredBirds2.length" scroll-y class="options-list">
				<view class="option-item" v-for="name in filteredBirds2" :key="`b2-${name}`" @click="selectBird(2, name)">
					{{ name }}
				</view>
			</scroll-view>
		</view>
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
			birds: [],
			query1: '',
			query2: '',
			showOptions1: false,
			showOptions2: false
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
		onQueryInput(type) {
			this[`showOptions${type}`] = true;
		},
		selectBird(type, name) {
			if (type === 1) {
				this.bird1 = name;
				this.query1 = name;
				this.showOptions1 = false;
				return;
			}
			this.bird2 = name;
			this.query2 = name;
			this.showOptions2 = false;
		},
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
		},
		filterBirdNames(query) {
			const q = (query || '').trim().toLowerCase();
			if (!q) return this.birdNames.slice(0, 20);
			return this.birdNames.filter(name => name.toLowerCase().includes(q)).slice(0, 20);
		}
	},
	computed: {
		filteredBirds1() {
			return this.filterBirdNames(this.query1);
		},
		filteredBirds2() {
			return this.filterBirdNames(this.query2);
		}
	}
};
</script>

<style scoped>
/* 样式部分：鸟类对比页面的布局和样式 */
.compare-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 24rpx; }
.title { font-size: 40rpx; font-weight: bold; color: #2d3436; }
.search-select { margin-bottom: 18rpx; position: relative; }
.search-input { background: #f5f5f5; border-radius: 8rpx; padding: 16rpx; color: #333; font-size: 28rpx; }
.options-list {
	max-height: 260rpx;
	background: #fff;
	border: 1rpx solid #e8e8e8;
	border-radius: 8rpx;
	margin-top: 8rpx;
}
.option-item { padding: 14rpx 16rpx; border-bottom: 1rpx solid #f1f1f1; color: #333; font-size: 26rpx; }
.option-item:last-child { border-bottom: none; }
.compare-result { margin-top: 24rpx; }
.compare-row { display: flex; gap: 18rpx; margin-bottom: 18rpx; }
.compare-col { flex: 1; background: #fff; border-radius: 12rpx; padding: 18rpx; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.03); }
.compare-label { color: #00b894; font-size: 16px; margin-bottom: 8rpx; display: block; }
.bird-img { width: 120rpx; height: 120rpx; border-radius: 12rpx; margin-bottom: 12rpx; background: #f5f5f5; }
</style>

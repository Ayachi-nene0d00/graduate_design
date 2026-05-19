<!-- encyclopedia.vue: 鸟类科普库页面，显示鸟类列表，包括图片和简介，点击进入详情页面 -->
<template>
	<view class="encyclopedia-page">
		<view class="header">
			<text class="title">鸟类科普库</text>
		</view>
		<view class="filter-bar">
			<input v-model="searchQuery" @input="searchBirds" placeholder="搜索鸟类" class="search-input" />
			<view class="filter-dropdowns">
				<picker :range="families" @change="filterByFamily" class="filter-picker">
					<view class="picker-content">
						<text class="picker-label">科属</text>
						<text class="picker-value">{{ selectedFamily || '全部' }}</text>
					</view>
				</picker>
				<picker :range="regions" @change="filterByRegion" class="filter-picker">
					<view class="picker-content">
						<text class="picker-label">地域</text>
						<text class="picker-value">{{ selectedRegion || '全部' }}</text>
					</view>
				</picker>
			</view>
		</view>
		<scroll-view scroll-y class="bird-list">
			<view class="bird-item" v-for="(bird, idx) in birds" :key="bird.name" @click="goDetail(bird)">
				<image :src="bird.img" class="bird-img" mode="aspectFill" />
				<view class="bird-info">
					<text class="bird-name">{{ bird.name }}</text>
					<text class="bird-brief">{{ bird.brief }}</text>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
// 脚本部分：加载鸟类数据并处理跳转到详情页面的逻辑
import { requestApi, getBaseUrl } from '@/common/api';
export default {
	data() {
		return {
			birds: [],
			searchQuery: '',
			selectedFamily: '',
			selectedRegion: '',
			families: [],
			regions: []
		};
	},
	onShow() {
		this.loadBirds();
		this.loadFilters();
	},
	methods: {
		async loadBirds() {
			try {
				let keyword = '';
				if (this.searchQuery) {
					keyword = this.searchQuery;
				} else if (this.selectedFamily) {
					keyword = this.selectedFamily;
				} else if (this.selectedRegion) {
					keyword = this.selectedRegion;
				}
				const path = keyword
					? `/api/bird?page=1&page_size=100&keyword=${encodeURIComponent(keyword)}`
					: '/api/bird?page=1&page_size=100';
				const res = await requestApi({ path, method: 'GET' });
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					this.birds = response.data.data.map(b => ({
						bird_id: b.bird_id,
						name: b.name,
						img: b.image_url ? (b.image_url.startsWith('http') ? b.image_url : getBaseUrl() + (b.image_url.startsWith('/') ? b.image_url : '/' + b.image_url)) : 'https://img.haoma.com/bird_placeholder.jpg',
						brief: b.feature || b.habit || '暂无描述'
					}));
					console.log('bird images:', this.birds.map(b => b.img));
				} else {
					this.birds = [];
				}
			} catch (e) {
				this.birds = [];
			}
		},
		async loadFilters() {
			try {
				const res = await requestApi({ path: '/api/bird?page=1&page_size=100', method: 'GET' });
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					const allBirds = response.data.data;
					this.families = [...new Set(allBirds.map(b => b.family).filter(f => f))];
					this.regions = [...new Set(allBirds.flatMap(b => b.region ? b.region.split(',') : []).filter(r => r))];
				}
			} catch (e) {
				// 忽略错误
			}
		},
		searchBirds() {
			this.loadBirds();
		},
		filterByFamily(e) {
			this.selectedFamily = this.families[e.detail.value];
			this.selectedRegion = '';
			this.searchQuery = '';
			this.loadBirds();
		},
		filterByRegion(e) {
			this.selectedRegion = this.regions[e.detail.value];
			this.selectedFamily = '';
			this.searchQuery = '';
			this.loadBirds();
		},
		goDetail(bird) {
			uni.navigateTo({
				url: `/pages/encyclopedia_detail?bird_id=${bird.bird_id}`
			});
		}
	}
};
</script>

<style scoped>
/* 样式部分：鸟类科普库页面的布局和样式 */
.encyclopedia-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 24rpx; }
.title { font-size: 40rpx; font-weight: bold; color: #2d3436; }
.filter-bar { display: flex; flex-direction: column; margin-bottom: 24rpx; }
.search-input {
  height: 60rpx;
  border: 1px solid #ddd;
  border-radius: 30rpx;
  padding: 0 20rpx;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 16rpx;
}
.filter-dropdowns { display: flex; justify-content: space-between; }
.filter-picker {
  flex: 1;
  margin-right: 8rpx;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 30rpx;
  padding: 10rpx 16rpx;
}
.picker-content { display: flex; justify-content: space-between; align-items: center; }
.picker-label { font-size: 24rpx; color: #666; }
.picker-value { font-size: 28rpx; color: #333; }
.bird-list { max-height: 70vh; }
.bird-item { display: flex; align-items: center; background: #fff; border-radius: 18rpx; margin-bottom: 18rpx; box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04); padding: 18rpx; }
.bird-img { width: 100rpx; height: 100rpx; border-radius: 12rpx; margin-right: 24rpx; }
.bird-info { flex: 1; }
.bird-name { font-size: 28rpx; font-weight: 500; color: #222; }
.bird-brief { font-size: 22rpx; color: #888; margin-top: 8rpx; display: block; }
</style>

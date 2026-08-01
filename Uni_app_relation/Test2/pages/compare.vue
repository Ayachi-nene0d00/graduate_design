<!-- compare.vue: 鸟类对比页面，用户可以选择两只鸟类进行对比，显示名称、习性、保护级别等信息 -->
<template>
	<view class="compare-page">
		<view class="header">
			<text class="title">鸟类对比</text>
		</view>
		<view class="selector-card">
			<text class="selector-title">鸟类1</text>
			<input
				v-model="search1"
				class="search-input"
				placeholder="输入名称模糊搜索鸟类1"
				@input="onInput1"
				@focus="onFocus1"
				@blur="onBlur1"
			/>
			<scroll-view v-if="showSuggestions1" scroll-y class="suggestion-list">
				<view
					v-for="name in filteredNames1"
					:key="`bird1-${name}`"
					class="suggestion-item"
					@tap="selectBird1(name)"
				>
					{{ name }}
				</view>
				<view v-if="!filteredNames1.length" class="suggestion-empty">未找到匹配鸟类</view>
			</scroll-view>
			<view class="picked-text">已选：{{ bird1 || '未选择' }}</view>
		</view>

		<view class="selector-card">
			<text class="selector-title">鸟类2</text>
			<input
				v-model="search2"
				class="search-input"
				placeholder="输入名称模糊搜索鸟类2"
				@input="onInput2"
				@focus="onFocus2"
				@blur="onBlur2"
			/>
			<scroll-view v-if="showSuggestions2" scroll-y class="suggestion-list">
				<view
					v-for="name in filteredNames2"
					:key="`bird2-${name}`"
					class="suggestion-item"
					@tap="selectBird2(name)"
				>
					{{ name }}
				</view>
				<view v-if="!filteredNames2.length" class="suggestion-empty">未找到匹配鸟类</view>
			</scroll-view>
			<view class="picked-text">已选：{{ bird2 || '未选择' }}</view>
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
const BLUR_DELAY_MS = 200;
const MAX_SUGGESTION_ITEMS = 20;
export default {
	data() {
		return {
			birdNames: [],
			bird1: '',
			bird2: '',
			birds: [],
			search1: '',
			search2: '',
			filteredNames1: [],
			filteredNames2: [],
			showSuggestions1: false,
			showSuggestions2: false,
			blurTimer1: null,
			blurTimer2: null
		};
	},
	onLoad() {
		this.loadBirds();
	},
	onUnload() {
		if (this.blurTimer1) clearTimeout(this.blurTimer1);
		if (this.blurTimer2) clearTimeout(this.blurTimer2);
		this.showSuggestions1 = false;
		this.showSuggestions2 = false;
	},
	methods: {
		async loadBirds() {
			try {
				const res = await requestApi({ path: '/api/bird?page=1&page_size=100', method: 'GET' });
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					this.birds = response.data.data;
					this.birdNames = this.birds.map(b => b.name);
					this.filteredNames1 = this.birdNames.slice(0, MAX_SUGGESTION_ITEMS);
					this.filteredNames2 = this.birdNames.slice(0, MAX_SUGGESTION_ITEMS);
				}
			} catch (e) {
				this.birds = [];
				this.birdNames = [];
				this.filteredNames1 = [];
				this.filteredNames2 = [];
			}
		},
		getFilteredNames(keyword) {
			const key = (keyword || '').trim().toLowerCase();
			const matched = key
				? this.birdNames.filter(name => name.toLowerCase().includes(key))
				: this.birdNames;
			return matched.slice(0, MAX_SUGGESTION_ITEMS);
		},
		onInput1(e) {
			const value = e.detail.value || '';
			this.search1 = value;
			this.filteredNames1 = this.getFilteredNames(value);
			this.showSuggestions1 = true;
		},
		onInput2(e) {
			const value = e.detail.value || '';
			this.search2 = value;
			this.filteredNames2 = this.getFilteredNames(value);
			this.showSuggestions2 = true;
		},
		onFocus1() {
			if (this.blurTimer1) clearTimeout(this.blurTimer1);
			this.filteredNames1 = this.getFilteredNames(this.search1);
			this.showSuggestions1 = true;
		},
		onFocus2() {
			if (this.blurTimer2) clearTimeout(this.blurTimer2);
			this.filteredNames2 = this.getFilteredNames(this.search2);
			this.showSuggestions2 = true;
		},
		onBlur1() {
			if (this.blurTimer1) clearTimeout(this.blurTimer1);
			this.blurTimer1 = setTimeout(() => {
				this.showSuggestions1 = false;
			}, BLUR_DELAY_MS);
		},
		onBlur2() {
			if (this.blurTimer2) clearTimeout(this.blurTimer2);
			this.blurTimer2 = setTimeout(() => {
				this.showSuggestions2 = false;
			}, BLUR_DELAY_MS);
		},
		selectBird1(name) {
			this.bird1 = name;
			this.search1 = name;
			this.showSuggestions1 = false;
		},
		selectBird2(name) {
			this.bird2 = name;
			this.search2 = name;
			this.showSuggestions2 = false;
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
		}
	}
};
</script>

<style scoped>
/* 样式部分：鸟类对比页面的布局和样式 */
.compare-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 24rpx; }
.title { font-size: 40rpx; font-weight: bold; color: #2d3436; }
.selector-card { background: #fff; border-radius: 12rpx; padding: 18rpx; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.03); margin-bottom: 18rpx; }
.selector-title { color: #00b894; font-size: 30rpx; font-weight: 600; display: block; margin-bottom: 10rpx; }
.search-input { background: #f5f5f5; border-radius: 8rpx; padding: 16rpx; color: #333; font-size: 28rpx; }
.suggestion-list { max-height: 260rpx; overflow: hidden; margin-top: 10rpx; border: 1rpx solid #f1f2f6; border-radius: 8rpx; }
.suggestion-item { padding: 14rpx 16rpx; border-bottom: 1rpx solid #f1f2f6; color: #2d3436; font-size: 26rpx; background: #fff; }
.suggestion-item:last-child { border-bottom: none; }
.suggestion-empty { padding: 14rpx 16rpx; color: #b2bec3; font-size: 24rpx; }
.picked-text { margin-top: 10rpx; color: #636e72; font-size: 24rpx; }
.compare-result { margin-top: 24rpx; }
.compare-row { display: flex; gap: 18rpx; margin-bottom: 18rpx; }
.compare-col { flex: 1; background: #fff; border-radius: 12rpx; padding: 18rpx; box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.03); }
.compare-label { color: #00b894; font-size: 16px; margin-bottom: 8rpx; display: block; }
.bird-img { width: 120rpx; height: 120rpx; border-radius: 12rpx; margin-bottom: 12rpx; background: #f5f5f5; }
</style>

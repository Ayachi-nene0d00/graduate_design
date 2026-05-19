<template>
	<view class="search-page">
		<view class="search-header">
			<view class="input-box">
				<text class="icon">🔍</text>
				<input 
					confirm-type="search" 
					v-model="keyword" 
					@confirm="doSearch(keyword)" 
					placeholder="输入鸟类名称，如：信天翁" 
					focus 
				/>
				<text v-if="keyword" class="clear" @click="keyword = ''">×</text>
				<text class="ai-btn" @click="goToAIQA">问AI</text>
			</view>
			<text class="cancel-btn" @click="goBack">取消</text>
		</view>

		<view class="section" v-if="localSearchHistory.length > 0">
			<view class="section-title">
				<text>历史搜索</text>
				<text class="delete-icon" @click="clearSearchHistory">🗑️</text>
			</view>
			<view class="tag-container">
				<view 
					class="tag" 
					v-for="(item, index) in localSearchHistory" 
					:key="index" 
					@click="doSearch(item)"
				>{{ item }}</view>
			</view>
		</view>

		<view class="section">
			<view class="section-title">热门发现</view>
			<view class="tag-container">
				<view class="tag hot" v-for="hot in hotBirds" :key="hot" @click="doSearch(hot)">
					🔥 {{ hot }}
				</view>
			</view>
		</view>

		<view class="section" v-if="loading">
			<view class="section-title">搜索中...</view>
		</view>

		<view class="section" v-else-if="results.length > 0">
			<view class="section-title">搜索结果</view>
			<view class="result-list">
				<view class="result-item" v-for="bird in results" :key="bird.bird_id" @click="goDetail(bird)">
					<image :src="bird.image_url || 'https://img.haoma.com/bird_placeholder.jpg'" class="result-img" mode="aspectFill" />
					<view class="result-info">
						<text class="result-name">{{ bird.name }}</text>
						<text class="result-brief">{{ bird.feature || bird.habit || '暂无简介' }}</text>
					</view>
				</view>
			</view>
		</view>

		<view class="tips">
			提示：搜索结果来自本地科普库，可点击查看详情
		</view>
	</view>
</template>

<script>
import { requestApi } from '@/common/api';
export default {
	data() {
		return {
			keyword: '',
			localSearchHistory: [],
			hotBirds: ['信天翁', '蜂鸟', '企鹅', '翠鸟', '火烈鸟', '天鹅'],
			results: [],
			loading: false
		};
	},
  onLoad(options) {
    if (options && options.keyword) {
      this.keyword = decodeURIComponent(options.keyword);
      this.doSearch(this.keyword);
    }
  },
	onShow() {
		this.localSearchHistory = uni.getStorageSync('search_history') || [];
	},
	methods: {
		async doSearch(k) {
			if (!k.trim()) return;
			
			// 1. 保存搜索历史
			let history = uni.getStorageSync('search_history') || [];
			history = history.filter(item => item !== k); // 去重
			history.unshift(k);
			history = history.slice(0, 10); // 只留10条
			uni.setStorageSync('search_history', history);
      this.localSearchHistory = history;

			this.loading = true;
			try {
				const res = await requestApi({
					path: `/api/bird?page=1&page_size=20&keyword=${encodeURIComponent(k)}`,
					method: 'GET'
				});
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					this.results = response.data.data;
				} else {
					this.results = [];
					uni.showToast({ title: '搜索失败', icon: 'none' });
				}
			} catch (e) {
				this.results = [];
				uni.showToast({ title: '网络请求失败', icon: 'none' });
			} finally {
				this.loading = false;
			}
		},
		clearSearchHistory() {
			uni.removeStorageSync('search_history');
			this.localSearchHistory = [];
		},
		goBack() {
			uni.navigateBack();
		},
		goToAIQA() {
			uni.navigateTo({
				url: '/pages/aiqa'
			});
		},
		goDetail(bird) {
			uni.navigateTo({
				url: `/pages/encyclopedia_detail?bird_id=${bird.bird_id}`
			});
		}
	}
}
</script>

<style scoped>
.search-page { padding: 30rpx; background: #fff; min-height: 100vh; }

.search-header { display: flex; align-items: center; gap: 20rpx; margin-bottom: 40rpx; }
.input-box { 
	flex: 1; background: #f1f2f6; height: 80rpx; border-radius: 40rpx; 
	display: flex; align-items: center; padding: 0 30rpx; 
}
.input-box input { flex: 1; font-size: 28rpx; margin-left: 15rpx; }
.cancel-btn { font-size: 28rpx; color: #00b894; }
.ai-btn {
	font-size: 28rpx; color: #0984e3;
	cursor: pointer;
}

.section { margin-bottom: 50rpx; }
.section-title { 
	display: flex; justify-content: space-between; align-items: center;
	font-size: 30rpx; font-weight: bold; color: #2d3436; margin-bottom: 25rpx; 
}
.tag-container { display: flex; flex-wrap: wrap; gap: 20rpx; }
.tag { 
	background: #f1f2f6; padding: 12rpx 30rpx; border-radius: 30rpx; 
	font-size: 24rpx; color: #636e72; 
}
.tag.hot { background: #fff5f5; color: #ff7675; border: 1rpx solid #ffecec; }

.result-list { display: flex; flex-direction: column; gap: 16rpx; }
.result-item { display: flex; align-items: center; background: #fff; border-radius: 16rpx; padding: 16rpx; box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.06); }
.result-img { width: 96rpx; height: 96rpx; border-radius: 12rpx; margin-right: 16rpx; }
.result-info { flex: 1; }
.result-name { font-size: 28rpx; font-weight: bold; color: #2d3436; display: block; }
.result-brief { font-size: 22rpx; color: #7f8c8d; margin-top: 6rpx; display: block; }

.tips { text-align: center; font-size: 22rpx; color: #b2bec3; margin-top: 100rpx; }
.delete-icon { font-size: 30rpx; padding: 10rpx; }
</style>
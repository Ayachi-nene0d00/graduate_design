<!-- history.vue: 历史记录页面，显示鸟类识别的历史记录，包括图片、名称、时间、置信度，支持删除和清空操作 -->
<template>
	<view class="history-page">
		<view class="header-action">
			<text class="title">📜 我的观鸟记录</text>
			<view class="action-right">
				<text class="count">共 {{ historyList.length }} 只</text>
				<text v-if="historyList.length > 0" class="clear-btn" @click="clearAll">垃圾箱 🗑️</text>
			</view>
		</view>

		<view v-if="historyList.length === 0" class="empty-state">
			<view class="empty-emoji">🐣</view>
			<text class="empty-text">这里空空如也，去发现你的第一只小鸟吧~</text>
			<button class="go-btn" @click="goHome">🚀 立即探索</button>
		</view>

		<scroll-view v-else scroll-y class="list-container">
			<view class="item-wrapper" v-for="(item, index) in historyList" :key="index">
				<view class="history-item" @click="reView(item)">
					<view class="img-wrapper">
						<image :src="item.img" mode="aspectFill" class="thumb"></image>
						<view class="conf-badge" :style="{ background: getConfColor(item.conf) }">
							{{ (item.conf * 100).toFixed(1) }}%
						</view>
					</view>
					<view class="info">
						<text class="name">🦅 {{ formatName(item.name) }}</text>
						<text class="time">📅 {{ item.time }}</text>
					</view>
					<view class="res">
						<view class="action-btn view-btn">👀 查看</view>
						<view class="action-btn del-btn" @click.stop="deleteItem(index)">❌ 删除</view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
// 脚本部分：加载、删除、清空历史记录，并处理跳转到分享页查看详情
import { requestApi } from '@/common/api';
import { formatBirdDisplayName, localizeBirdName } from '@/common/bird_name_localizer';

export default {
	data() {
		return {
			historyList: []
		};
	},
	onShow() {
		this.loadHistory();
	},
	methods: {
		async loadHistory() {
			const originHistory = uni.getStorageSync('bird_history') || [];
			let changed = false;
			this.historyList = await Promise.all(originHistory.map(async (item) => {
				const localizedName = await localizeBirdName(item.name, requestApi);
				if (localizedName === item.name) return item;
				changed = true;
				return { ...item, name: localizedName };
			}));
			if (changed) {
				uni.setStorageSync('bird_history', this.historyList);
			}
		},
		formatName(name) {
			return formatBirdDisplayName(name);
		},
		getConfColor(conf) {
			if(conf >= 0.9) return '#00b894';
			if(conf >= 0.6) return '#fdcb6e';
			return '#ff7675';
		},
		goHome() {
			uni.navigateBack();
		},
		handleImageError() {
			// 如果占位图加载失败，什么都不做
		},
		deleteItem(index) {
			uni.showModal({
				title: '删除记录',
				content: '确认删除这条神奇的发现吗？',
				confirmColor: '#ff7675',
				success: (res) => {
					if (res.confirm) {
						this.historyList.splice(index, 1);
						uni.setStorageSync('bird_history', this.historyList);
					}
				}
			});
		},
		clearAll() {
			uni.showModal({
				title: '清空历史',
				content: '所有记录将被永久删除，确定吗？',
				confirmColor: '#ff7675',
				success: (res) => {
					if (res.confirm) {
						this.historyList = [];
						uni.removeStorageSync('bird_history');
					}
				}
			});
		},
		reView(item) {
			// 点击历史记录跳转回分享页查看详情
			uni.navigateTo({
				url: `/pages/share/share?name=${item.name}&conf=${item.conf}&img=${encodeURIComponent(item.img)}`
			});
		}
	}
}
</script>

<style scoped>
/* 样式部分：历史记录页面的布局和样式 */
.history-page { padding: 40rpx 30rpx; background: #f4f6f8; min-height: 100vh; }
.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40rpx; padding: 0 10rpx; }
.title { font-size: 44rpx; font-weight: 800; color: #2d3436; }
.action-right { display: flex; align-items: center; gap: 20rpx; }
.count { font-size: 24rpx; color: #636e72; background: #dfe6e9; padding: 6rpx 16rpx; border-radius: 20rpx; }
.clear-btn { font-size: 24rpx; color: #ff7675; padding: 6rpx 16rpx; border: 1rpx solid #fab1a0; border-radius: 20rpx; }

.empty-state { text-align: center; margin-top: 150rpx; display: flex; flex-direction: column; align-items: center; }
.empty-emoji { font-size: 60rpx; margin-bottom: 20rpx; }
.empty-text { color: #b2bec3; font-size: 28rpx; margin-bottom: 40rpx; }
.go-btn { background: #87CEEB; color: #fff; width: 240rpx; height: 70rpx; line-height: 70rpx; font-size: 28rpx; border-radius: 35rpx; border: none; box-shadow: 0 8rpx 15rpx rgba(135, 206, 235, 0.3); }

.list-container { padding-bottom: 50rpx; }

.history-item {
	background: #ffffff; border-radius: 30rpx; padding: 24rpx; margin-bottom: 24rpx;
	display: flex; align-items: center; box-shadow: 0 8rpx 20rpx rgba(0,0,0,0.03);
	transition: all 0.2s ease;
}
.history-item:active { transform: scale(0.98); }

.img-wrapper { position: relative; margin-right: 24rpx; }
.thumb { width: 140rpx; height: 140rpx; border-radius: 20rpx; background: #f1f2f6; box-shadow: 0 4rpx 10rpx rgba(0,0,0,0.05); }
.conf-badge {
	position: absolute; bottom: -10rpx; left: 50%; transform: translateX(-50%);
	color: #fff; font-size: 18rpx; font-weight: bold; padding: 4rpx 12rpx; border-radius: 12rpx;
	white-space: nowrap; box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.2);
}

.info { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.name { font-size: 32rpx; font-weight: 800; color: #2d3436; margin-bottom: 6rpx; }
.time { font-size: 22rpx; color: #a4b0be; }

.res { display: flex; flex-direction: column; align-items: flex-end; gap: 16rpx; }
.action-btn { font-size: 22rpx; padding: 8rpx 24rpx; border-radius: 16rpx; text-align: center; }
.view-btn { background: #e3f2fd; color: #87CEEB; font-weight: bold; }
.del-btn { background: #ffeaa7; color: #d63031; }
</style>

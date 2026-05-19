<!-- encyclopedia_detail.vue: 鸟类百科详情页面，显示选中鸟类的图片、简介、习性、保护级别等详细信息 -->
<template>
	<view class="ency-detail-page">
		<view class="header">
			<text class="title">{{ bird.name }}</text>
		</view>
		<image :src="bird.img" class="bird-img" mode="aspectFill" />
		<view class="section">
			<text class="section-title">简介</text>
			<text class="section-content">{{ bird.brief }}</text>
		</view>
		<view class="section">
			<text class="section-title">习性</text>
			<text class="section-content">{{ bird.habit || '暂无数据' }}</text>
		</view>
		<view class="section">
			<text class="section-title">保护级别</text>
			<text class="section-content">{{ bird.protect || '暂无数据' }}</text>
		</view>
	</view>
</template>

<script>
// 脚本部分：根据传递的参数加载鸟类详情数据
import { requestApi, getBaseUrl } from '@/common/api';
export default {
	data() {
		return { bird: {} };
	},
	async onLoad(options) {
		const birdId = options.bird_id;
		if (!birdId) {
			this.bird = {
				name: '未知',
				img: 'https://img.haoma.com/bird_placeholder.jpg',
				brief: '暂无简介',
				habit: '',
				protect: ''
			};
			return;
		}
		try {
			const res = await requestApi({ path: `/api/bird/${birdId}`, method: 'GET' });
			const response = res.data ? res : (res[1] || {});
			if (response.statusCode === 200 && response.data && response.data.code === 0) {
				const data = response.data.data;
				this.bird = {
					name: data.name,
					img: data.image_url ? (data.image_url.startsWith('http') ? data.image_url : getBaseUrl() + (data.image_url.startsWith('/') ? data.image_url : '/' + data.image_url)) : 'https://img.haoma.com/bird_placeholder.jpg',
					brief: data.feature || '暂无简介',
					habit: data.habit || '',
					protect: data.protect_level || ''
				};
			} else {
				this.bird = { name: '未知', img: 'https://img.haoma.com/bird_placeholder.jpg', brief: '暂无简介' };
			}
		} catch (e) {
			this.bird = { name: '未知', img: 'https://img.haoma.com/bird_placeholder.jpg', brief: '暂无简介' };
		}
	}
};
</script>

<style scoped>
/* 样式部分：鸟类百科详情页面的布局和样式 */
.ency-detail-page { padding: 32rpx; }
.header { text-align: center; margin-bottom: 24rpx; }
.title { font-size: 38rpx; font-weight: bold; color: #2d3436; }
.bird-img { width: 100%; height: 320rpx; border-radius: 18rpx; margin-bottom: 24rpx; background: #f5f5f5; }
.section { margin-bottom: 24rpx; }
.section-title { font-size: 26rpx; color: #00b894; font-weight: 500; margin-bottom: 8rpx; display: block; }
.section-content { font-size: 22rpx; color: #333; }
</style>

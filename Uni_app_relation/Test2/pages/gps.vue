<!-- gps.vue: GPS推荐页面，用户点击获取推荐后，模拟定位并显示当前位置常见的鸟类列表 -->
<template>
        <view class="gps-page">
                <view class="header">
                        <text class="title">📍 本地鸟类推荐</text>
                </view>

                <view class="location-box">
			<view class="location-header">
				<text class="desc">当前定位区域：<text class="highlight-city">{{ currentCity || '未知' }}</text></text>
				<!-- 增加手动选择省市的 picker -->
				<picker mode="region" @change="onRegionChange" class="region-picker">
					<text class="manual-select">手动选择 🌍</text>
				</picker>
			</view>

			<button class="gps-btn" @click="getLocation" :disabled="loading" :class="{'btn-loading': loading}">
				<text v-if="!loading">重新GPS定位获取</text>
				<text v-else>定位及加载中...</text>
			</button>
		</view>

                <view v-if="birds.length > 0" class="recommend-box">
                        <text class="section-title">✨ 今日推荐</text>
                        <!-- 这里的轮播效果即为需求中的“轮播” -->
                        <swiper class="bird-swiper" :indicator-dots="true" :autoplay="true" :interval="carouselInterval" :circular="true">
                                <swiper-item v-for="(bird, index) in birds" :key="index">
                                        <view class="bird-card">
                        <image :src="bird.image_url" class="bird-img" mode="aspectFill" @click="previewImg(bird.image_url)" @error="onImgError(index)" />
						<view class="bird-info">
							<text class="bird-name">{{ bird.name }} <text class="bird-en-name" v-if="bird.english_name">({{ bird.english_name }})</text></text>
							<text class="bird-family">所属科属：{{ bird.family || '未知' }} | 保护级别：<text class="level-tag">{{ bird.protect_level || '无' }}</text></text>

							<view class="info-group">
								<text class="info-label">📍 分布区域：</text>
								<text class="info-text">{{ bird.province || '' }} {{ bird.city || '' }} ({{ formatText(bird.region, 20) }})</text>
							</view>

							<view class="info-group">
								<text class="info-label">📝 外形特征：</text>
								<text class="info-text">{{ formatText(bird.feature, 40) }}</text>
							</view>
						</view>
					</view>
                                </swiper-item>
                        </swiper>
                </view>

                <view v-else-if="!loading" class="empty-state">
                        <text>点击上方按钮获取您附近的鸟类推荐~</text>
                </view>
        </view>
</template>

<script>
// 新增导入 getBaseUrl，和encyclopedia.vue保持一致
import { requestApi, getBaseUrl } from '@/common/api';
export default {
		data() {
		return {
			loading: false,
			birds: [],
			currentCity: '四川', // 默认省份
			carouselInterval: 3000 // 默认轮播间隔3秒
		};
	},
	onLoad() {
		// 页面加载时自动请求一次推荐
		this.fetchRecommendations(this.currentCity);

		// 尝试从本地存储读取用户自定义的轮播间隔时间 (如果有)
		const userSetting = uni.getStorageSync('user_setting');
		if (userSetting && userSetting.carousel_interval) {
			this.carouselInterval = userSetting.carousel_interval * 1000;
		}
	},
	methods: {
		getLocation() {
			this.loading = true;
			uni.getLocation({
				type: 'gcj02',
				geocode: true,
				success: (res) => {
					console.log('Location success:', res);
					let city = '四川';
					if (res.address && res.address.province) {
						// 优先使用省份，因为主要按Province来分
						city = res.address.province.replace('省', '').replace('市', '');
					} else if (res.address && res.address.city) {
						city = res.address.city.replace('市', '');
					}
					this.currentCity = city;
					this.fetchRecommendations(city);
				},
				fail: (err) => {
					console.error('Location fail:', err);
					uni.showToast({ title: 'GPS获取失败，您可以尝试手动选择区域', icon: 'none', duration: 3000 });

					// 如果失败，调用一个免费的IP定位API作为后备
					uni.request({
						url: 'http://ip-api.com/json/?lang=zh-CN',
						method: 'GET',
						success: (ipRes) => {
							if (ipRes.statusCode === 200 && ipRes.data && ipRes.data.regionName) {
								let city = ipRes.data.regionName.replace('省', '').replace('市', '');
								this.currentCity = city;
								uni.showToast({ title: `已通过网络定位到: ${city}`, icon: 'none' });
								this.fetchRecommendations(city);
							} else {
								this.fetchRecommendations(this.currentCity);
							}
						},
						fail: () => {
							this.fetchRecommendations(this.currentCity);
						}
					});
				}
			});
		},
		onRegionChange(e) {
			// e.detail.value 是一个数组：[省, 市, 区]
			const province = e.detail.value[0].replace('省', '').replace('市', '');
			const city = e.detail.value[1].replace('市', '');

			// 优先采用省份检索，因为数据库更倾向于Province匹配
			this.currentCity = province;
			uni.showToast({ title: `已手动切换至 ${province}`, icon: 'success' });
			this.fetchRecommendations(province);
		},
		async fetchRecommendations(city) {
			this.loading = true;
				if (uni.getStorageSync('gps_city') !== city) {
				uni.setStorageSync('gps_city', city);
			}
			try {
				const res = await requestApi({
					path: `/api/recommend?city=${encodeURIComponent(city)}`,
					method: 'GET',
					timeout: 5000
				});
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data.code === 0) {
					// 核心修改：按照encyclopedia.vue的逻辑处理图片URL
					this.birds = response.data.data.map(b => ({
						...b,
						image_url: b.image_url
							? (b.image_url.startsWith('http')
								? b.image_url
								: getBaseUrl() + (b.image_url.startsWith('/') ? b.image_url : '/' + b.image_url))
							: 'https://img.haoma.com/bird_placeholder.jpg'
					}));
				} else {
					uni.showToast({ title: '获取推荐数据失败', icon: 'none' });
				}
			} catch (e) {
				console.error('Fetch error:', e);
				uni.showToast({ title: '网络请求失败，请检查后端', icon: 'none' });
			} finally {
				this.loading = false;
			}
		},
		formatText(text, length) {
			if (!text) return '暂无数据';
			return text.length > length ? text.substring(0, length) + '...' : text;
		},
		onImgError(index) {
			// 图片加载失败时兜底，和encyclopedia.vue保持一致
			this.birds[index].image_url = 'https://img.haoma.com/bird_placeholder.jpg';
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
.gps-page { padding: 30rpx 20rpx; min-height: 100vh; background: #f0f4f8; font-family: 'Helvetica Neue', Helvetica, sans-serif; }
.header { text-align: center; margin-bottom: 30rpx; margin-top: 20rpx; }
.title { font-size: 50rpx; font-weight: 900; color: #2c3e50; letter-spacing: 2rpx; }

.location-box { background: #ffffff; padding: 40rpx 30rpx; border-radius: 30rpx; box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.06); margin-bottom: 40rpx; }
.location-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30rpx; }
.desc { font-size: 32rpx; color: #34495e; font-weight: bold; }
.highlight-city { color: #e74c3c; font-size: 36rpx; margin-left: 10rpx; }
.region-picker { background: #ecf0f1; padding: 10rpx 20rpx; border-radius: 20rpx; }
.manual-select { font-size: 26rpx; color: #2980b9; font-weight: bold; }

.gps-btn {
	background: linear-gradient(135deg, #3498db, #2980b9);
	color: #fff;
	border-radius: 50rpx;
	padding: 10rpx 0;
	font-size: 32rpx;
	font-weight: bold;
	width: 100%;
	box-shadow: 0 8rpx 20rpx rgba(52, 152, 219, 0.4);
	border: none;
}
.gps-btn::after { border: none; }
.gps-btn:active { transform: scale(0.98); }
.btn-loading { background: #95a5a6; box-shadow: none; pointer-events: none; }

.recommend-box { margin-top: 20rpx; animation: fadeIn 0.6s ease; }
.section-title { font-size: 38rpx; font-weight: 900; color: #2c3e50; margin-bottom: 30rpx; display: block; padding-left: 16rpx; border-left: 10rpx solid #e74c3c; }

.bird-swiper { height: 900rpx; width: 100%; border-radius: 30rpx; overflow: hidden; box-shadow: 0 15rpx 35rpx rgba(0,0,0,0.1); }
.bird-card { background: #ffffff; height: 100%; display: flex; flex-direction: column; border-radius: 30rpx; }
.bird-img { width: 100%; height: 480rpx; background-color: #f5f6fa; object-fit: cover; }
.bird-info { padding: 30rpx; flex: 1; display: flex; flex-direction: column; }
.bird-name { font-size: 44rpx; font-weight: 900; color: #2d3436; margin-bottom: 6rpx; display: flex; align-items: center;}
.bird-en-name { font-size: 26rpx; color: #b2bec3; font-weight: normal; margin-left: 10rpx; font-style: italic; }
.bird-family { font-size: 28rpx; color: #636e72; margin-bottom: 24rpx; font-weight: 600; padding-bottom: 20rpx; border-bottom: 2rpx dashed #dfe6e9; }
.level-tag { background: #ffeaa7; color: #d63031; padding: 4rpx 16rpx; border-radius: 20rpx; font-size: 24rpx; font-weight: bold; }

.info-group { margin-bottom: 16rpx; }
.info-label { font-size: 28rpx; font-weight: bold; color: #00b894; }
.info-text { font-size: 28rpx; color: #2d3436; line-height: 1.6; }

.empty-state { text-align: center; margin-top: 150rpx; color: #b2bec3; font-size: 32rpx; animation: fadeIn 0.5s ease; }

@keyframes fadeIn {
	from { opacity: 0; transform: translateY(10rpx); }
	to { opacity: 1; transform: translateY(0); }
}
</style>

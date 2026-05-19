<template>
  <view class="quiz-bird-list">
    <view v-for="bird in birds" :key="bird.bird_id || bird.id" class="quiz-bird-item" @click="goDetail(bird)">
      <image :src="getImg(bird)" class="quiz-bird-img" mode="aspectFill" />
      <text class="quiz-bird-name">{{ bird.name || bird.english_name || '未知鸟类' }}</text>
    </view>
  </view>
</template>

<script>
import { getBaseUrl } from '@/common/api';
export default {
  props: {
    birds: { type: Array, default: () => [] }
  },
  methods: {
    getImg(bird) {
      const url = bird.image_url || '';
      if (!url) return 'https://img.haoma.com/bird_placeholder.jpg';
      if (url.startsWith('http')) return url;
      return getBaseUrl() + (url.startsWith('/') ? url : '/' + url);
    },
    goDetail(bird) {
      const id = bird.bird_id || bird.id;
      if (!id) return;
      uni.navigateTo({ url: `/pages/encyclopedia_detail?bird_id=${id}` });
    }
  }
};
</script>

<style scoped>
.quiz-bird-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin: 32rpx 0;
}
.quiz-bird-item {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 18rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
  padding: 18rpx;
  cursor: pointer;
}
.quiz-bird-img {
  width: 100rpx;
  height: 100rpx;
  border-radius: 12rpx;
  margin-right: 24rpx;
  background: #f5f5f5;
}
.quiz-bird-name {
  font-size: 28rpx;
  font-weight: 500;
  color: #222;
}
</style>

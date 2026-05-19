<!-- aiqa.vue: AI问答页面，用户可以输入鸟类相关问题，提交后获取AI模拟回答 -->
<template>
	<view class="aiqa-page">
		<view class="header">
			<text class="title">🐦 AI 鸟类百科</text>
			<text class="subtitle">您的私人自然专家，有问必答</text>
		</view>

		<view class="qa-section">
			<view class="input-wrapper">
				<input
					v-model="question"
					class="qa-input"
					placeholder="例如：蜂鸟一天吃多少东西？"
					@confirm="askAI"
					confirm-type="send"
				/>
				<button class="qa-btn" @click="askAI" :disabled="loading" :class="{'btn-loading': loading}">
					<text v-if="!loading">发送</text>
					<text v-else>思考中</text>
				</button>
			</view>
		</view>

		<!-- 初始空白提示 -->
		<view class="empty-state" v-if="!answer && !loading">
			<view class="empty-icon">🦉</view>
			<text class="empty-text">快来向我提问吧！</text>
			<view class="tag-list">
				<text class="suggest-tag" @click="question='信天翁能飞多远？'">信天翁能飞多远？</text>
				<text class="suggest-tag" @click="question='中国有哪些保护鸟类？'">中国有哪些保护鸟类？</text>
				<text class="suggest-tag" @click="question='如何区分燕子和麻雀？'">如何区分燕子和麻雀？</text>
			</view>
		</view>

		<view class="chat-container" v-if="answer || loading">
			<!-- 用户的提问气泡 -->
			<view class="message-row user-row" v-if="submittedQuestion">
				<view class="bubble user-bubble">
					<text>{{ submittedQuestion }}</text>
				</view>
				<view class="avatar user-avatar">我</view>
			</view>

			<!-- AI 的回答气泡 -->
			<view class="message-row ai-row">
				<view class="avatar ai-avatar">AI</view>
				<view class="bubble ai-bubble" :class="{'thinking': loading}">
					<text v-if="!loading">{{ answer }}</text>
					<view v-else class="loading-wrapper">
						<view class="spinner"></view>
						<text class="typing-text">{{ randomLoadingText }}</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { requestApi } from '@/common/api';
export default {
	data() {
		return {
			question: '',
			submittedQuestion: '', // 记录当前提交的问题
			answer: '',
			loading: false,
			loadingInterval: null,
			randomLoadingText: '正在和猫头鹰核对数据...',
			loadingTexts: [
				'正在给鸽子发报请求支援...',
				'正在翻译复杂的鸟语...',
				'正跨过山和大海找寻这只鸟...',
				'跟猫头鹰连线核对数据中...',
				'翻阅《百年野生鸟类绝密档案》...',
				'让翠鸟帮我出去探探风...',
				'喂？鹦鹉吗？帮我查一下这个...'
			]
		};
	},
	methods: {
		async askAI() {
			if (!this.question.trim()) {
				uni.showToast({ title: '请输入问题', icon: 'none' });
				return;
			}
			this.submittedQuestion = this.question;
			this.loading = true;
			this.answer = '';

			// 趣味加载文案轮播
			let textIdx = 0;
			this.randomLoadingText = this.loadingTexts[textIdx];
			this.loadingInterval = setInterval(() => {
				textIdx = (textIdx + 1) % this.loadingTexts.length;
				this.randomLoadingText = this.loadingTexts[textIdx];
			}, 3000);

			// 提问后清空输入框提升体验
			const currentQ = this.question;
			this.question = '';

			try {
				const res = await requestApi({
					path: '/api/aiqa',
					method: 'POST',
					data: { question: currentQ },
					timeout: 120000
				});
				const response = res.data ? res : (res[1] ? res[1] : null);
				if (response && response.statusCode === 200 && response.data && response.data.code === 0) {
					this.answer = response.data.data.answer || '暂无回答';
				} else {
					console.error('AI接口返回异常', response);
					this.answer = 'AI服务暂时不可用，请稍后再试。';
				}
			} catch (e) {
				console.error('AI接口调用失败', e);
				this.answer = '服务请求失败，建议检查网络或使用离线兜底模式。';
			} finally {
				this.loading = false;
				if (this.loadingInterval) {
					clearInterval(this.loadingInterval);
					this.loadingInterval = null;
				}
			}
		}
	}
};
</script>

<style scoped>
/* 整个页面的底色与高级感 */
.aiqa-page {
	min-height: 100vh;
	background: #f4f7f6;
	padding: 40rpx 30rpx;
	font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 顶部标题区 */
.header { text-align: center; margin-bottom: 50rpx; margin-top: 20rpx; }
.title { font-size: 52rpx; font-weight: 900; color: #2c3e50; display: block; letter-spacing: 2rpx; }
.subtitle { font-size: 26rpx; color: #7f8c8d; margin-top: 12rpx; display: block; margin-bottom: 30rpx; }

/* 输入框区 */
.qa-section { margin-bottom: 40rpx; }
.input-wrapper {
	display: flex;
	align-items: center;
	background: #ffffff;
	border-radius: 50rpx;
	padding: 10rpx 10rpx 10rpx 36rpx;
	box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.06);
	border: 2rpx solid #ecf0f1;
}
.qa-input { flex: 1; height: 70rpx; font-size: 30rpx; color: #34495e; outline: none; }
.qa-btn {
	background: linear-gradient(135deg, #00b894, #00cec9);
	color: #fff;
	border-radius: 40rpx;
	width: 160rpx;
	height: 74rpx;
	line-height: 74rpx;
	font-size: 28rpx;
	font-weight: bold;
	text-align: center;
	padding: 0;
	margin-left: 20rpx;
	box-shadow: 0 6rpx 15rpx rgba(0, 184, 148, 0.3);
}
.qa-btn::after { border: none; }
.btn-loading { background: #b2bec3; box-shadow: none; pointer-events: none; }

/* 初始状态提示区 */
.empty-state { text-align: center; margin-top: 100rpx; animation: fadeIn 0.8s ease; }
.empty-icon { font-size: 100rpx; line-height: 1; margin-bottom: 20rpx; }
.empty-text { font-size: 30rpx; color: #95a5a6; font-weight: 500; display: block; margin-bottom: 40rpx; }
.tag-list { display: flex; flex-direction: column; align-items: center; gap: 20rpx; }
.suggest-tag { background: #e8f8f5; color: #00b894; padding: 16rpx 32rpx; border-radius: 30rpx; font-size: 26rpx; border: 2rpx solid #c8e6c9; }
.suggest-tag:active { transform: scale(0.98); background: #d1f2eb; }

/* 聊天气泡布局区 */
.chat-container { display: flex; flex-direction: column; gap: 40rpx; padding-bottom: 40rpx; }
.message-row { display: flex; align-items: flex-start; width: 100%; animation: slideUp 0.4s ease; }
.user-row { justify-content: flex-end; }
.ai-row { justify-content: flex-start; }

.avatar {
	width: 72rpx;
	height: 72rpx;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: bold;
	font-size: 24rpx;
	color: #fff;
	flex-shrink: 0;
	box-shadow: 0 4rpx 10rpx rgba(0,0,0,0.1);
}
.user-avatar { background: #0984e3; margin-left: 16rpx; }
.ai-avatar { background: #00b894; margin-right: 16rpx; }

.bubble {
	max-width: 75%;
	padding: 24rpx 32rpx;
	font-size: 30rpx;
	line-height: 1.6;
	word-wrap: break-word;
	box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
}
.user-bubble {
	background: #0984e3;
	color: #ffffff;
	border-radius: 32rpx 4rpx 32rpx 32rpx;
}
.ai-bubble {
	background: #ffffff;
	color: #2d3436;
	border-radius: 4rpx 32rpx 32rpx 32rpx;
	border: 2rpx solid #f1f2f6;
}

.thinking { color: #b2bec3; font-style: italic; }
.loading-wrapper { display: flex; align-items: center; gap: 16rpx; }
.spinner {
	width: 32rpx;
	height: 32rpx;
	border: 4rpx solid #dfe6e9;
	border-top-color: #00b894;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	flex-shrink: 0;
}
.typing-text { animation: pulse 1.5s infinite; font-size: 28rpx; }

/* 简单动画 */
@keyframes spin {
	to { transform: rotate(360deg); }
}
@keyframes slideUp {
	from { opacity: 0; transform: translateY(20rpx); }
	to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
	from { opacity: 0; }
	to { opacity: 1; }
}
@keyframes pulse {
	0% { opacity: 0.6; }
	50% { opacity: 1; }
	100% { opacity: 0.6; }
}
</style>

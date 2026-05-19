<!-- quiz.vue: 鸟类Quiz问答页面，提供鸟类相关问题测试用户知识 -->
<template>
	<view class="quiz-page">
		<view class="header">
			<text class="title">🐦 鸟类Quiz问答 🎉</text>
			<view class="score-display" v-if="current > 0">得分：{{ score }} / {{ current }}</view>
		</view>
		<view v-if="current < questions.length">
			<view class="question">❓ {{ questions[current].q }}</view>
			<view class="options">
				<button v-for="(opt, idx) in questions[current].opts" :key="idx" class="option-btn" @click="choose(idx)">{{ opt }}</button>
			</view>
			<view v-if="showAnswer" class="answer">
				<text v-if="lastChoice === questions[current].a" class="correct">✅ 正确！</text>
				<text v-else class="wrong">❌ 错误！正确答案：{{ questions[current].opts[questions[current].a] }}</text>
			</view>
			<button v-if="showAnswer && current < questions.length-1" class="next-btn" @click="next">➡️ 下一题</button>
		</view>
		<view v-else-if="!completed" class="finish">
			<text class="finish-text">🎉 题目已答完！</text>
			<button class="complete-btn" @click="completeQuiz">🏆 完成！</button>
			<button class="play-again-btn">🎮 再玩一次</button>
		</view>
		<view v-else class="result">
			<view class="result-header">
				<text class="result-title">🎊 答题完成！</text>
				<text class="final-score">你的得分：{{ score }} / {{ questions.length }}</text>
			</view>
			<view class="history-section">
				<text class="history-title">📜 答题历史</text>
				<view class="history-list">
					<view v-for="(item, idx) in quizHistory" :key="idx" class="history-item">
						<text class="history-q">{{ item.question }}</text>
						<text :class="item.correct ? 'correct-icon' : 'wrong-icon'">{{ item.correct ? '✅' : '❌' }}</text>
					</view>
				</view>
			</view>
			<button class="retry-btn" @click="retryQuiz">🔄 再来一次</button>
		</view>
		<button class="exit-btn" @click="exitQuiz">🏃‍♂️ 退出问答</button>
		<view class="quiz-history">
			<text class="history-title">📜 历史记录</text>
			<view class="history-list">
				<view v-for="(record, idx) in quizHistoryList" :key="idx" class="history-record">
					<text>{{ record.date }} - 得分：{{ record.score }}/{{ record.total }}</text>
				</view>
			</view>
		</view>
		<view v-if="completed && quizBirds.length" class="quiz-bird-list-section">
			<text class="history-title">本次涉及鸟类</text>
			<QuizBirdList :birds="quizBirds" />
		</view>
	</view>
</template>

<script>
// 脚本部分：处理Quiz问题选择、显示答案、下一题、完成逻辑和历史记录
import { requestApi } from '@/common/api';
import QuizBirdList from '@/components/QuizBirdList.vue';
export default {
	data() {
		return {
			questions: [],
			current: 0,
			showAnswer: false,
			score: 0,
			quizHistory: [],
			completed: false,
			lastChoice: -1,
			quizHistoryList: [],
			// 在data中增加本次涉及鸟类数组
			quizBirds: []
		};
	},
	onLoad() {
		this.quizHistoryList = uni.getStorageSync('quiz_history') || [];
		this.loadQuiz();
	},
	methods: {
		async loadQuiz() {
			// 骨架屏提示或Loading效果
			uni.showLoading({ title: '加载题库中...', mask: true });

			// 生成5道基于数据库字段设计的内置题库作为替补（当未接入数据库API时直接使用）
			const dbMockQuestions = [
				{ q: '世界上飞得最快的鸟是哪一种？ (debug)', opts: ['游隼', '鸵鸟', '蜂鸟', '老鹰'], a: 0 },
				{ q: '以下哪种鸟类不会飞？ (debug)', opts: ['麻雀', '乌鸦', '企鹅', '燕子'], a: 2 },
				{ q: '世界上最小的鸟是？ (debug)', opts: ['喜鹊', '吸蜜蜂鸟', '知更鸟', '画眉'], a: 1 },
				{ q: '哪种鸟类以能够在空中倒飞而闻名？ (debug)', opts: ['鸽子', '鹦鹉', '孔雀', '蜂鸟'], a: 3 },
				{ q: '企鹅主要生活在哪个地区？ (debug)', opts: ['北极', '赤道', '南极', '沙漠'], a: 2 }
			];

			try {
				const res = await requestApi({ path: '/api/quiz', method: 'GET', timeout: 5000 });
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data.code === 0 && response.data.data.length > 0) {
					// 从真正的数据库返回题库并映射
					let apiQuestions = response.data.data.map(q => ({
						q: q.question,
						opts: [q.option_a, q.option_b, q.option_c, q.option_d],
						a: q.correct_answer.trim().toUpperCase().charCodeAt(0) - 65
					}));

					// 如果不足 5 题，用备用的充满
					if (apiQuestions.length < 5) {
						let mockData = dbMockQuestions.sort(() => 0.5 - Math.random());
						apiQuestions = apiQuestions.concat(mockData).slice(0, 5);
					}
					this.questions = apiQuestions;
				} else {
					this.questions = dbMockQuestions.sort(() => 0.5 - Math.random()).slice(0, 5);
				}
			} catch (e) {
				console.error('Quiz fetch error:', e);
				this.questions = dbMockQuestions.sort(() => 0.5 - Math.random()).slice(0, 5);
			} finally {
				uni.hideLoading();
			}
		},
		choose(idx) {
			this.lastChoice = idx;
			this.showAnswer = true;
			if (idx === this.questions[this.current].a) {
				this.score++;
			}
			// 如果是最后一题，自动完成
			if (this.current === this.questions.length - 1) {
				this.completeQuiz();
			}
		},
		next() {
			this.quizHistory.push({
				question: this.questions[this.current].q,
				correct: this.lastChoice === this.questions[this.current].a
			});
			this.current++;
			this.showAnswer = false;
			this.lastChoice = -1;
		},
		completeQuiz() {
			this.quizHistory.push({
				question: this.questions[this.current].q,
				correct: this.lastChoice === this.questions[this.current].a
			});
			this.completed = true;
			// 统计本次Quiz涉及的所有鸟类（从题干或选项中提取，假设题干或选项含有鸟名）
			const birdNames = new Set();
			this.questions.forEach(q => {
				// 简单正则提取题干和选项中的鸟名
				[q.q, ...(q.opts || [])].forEach(str => {
					if (typeof str === 'string') {
						// 假设鸟名为2-8个汉字或英文单词
						(str.match(/[\u4e00-\u9fa5A-Za-z_\- ]{2,20}/g) || []).forEach(n => birdNames.add(n.trim()));
					}
				});
			});
			// 用百科接口查找所有相关鸟类详细信息
			requestApi({ path: '/api/bird?page=1&page_size=400', method: 'GET' }).then(res => {
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					this.quizBirds = response.data.data.filter(b => birdNames.has(b.name) || birdNames.has(b.english_name));
				} else {
					this.quizBirds = [];
				}
			});
			// 保存历史到本地存储
			let history = uni.getStorageSync('quiz_history') || [];
			history.unshift({
				date: new Date().toLocaleString(),
				score: this.score,
				total: this.questions.length,
				history: this.quizHistory
			});
			uni.setStorageSync('quiz_history', history.slice(0, 10)); // 保留最近10次
		},
		retryQuiz() {
			this.current = 0;
			this.score = 0;
			this.quizHistory = [];
			this.completed = false;
			this.showAnswer = false;
			this.lastChoice = -1;
		},
		exitQuiz() {
			uni.showModal({
				title: '😢 确定要离开吗？',
				content: '鸟类知识等你回来哦！',
				success: (res) => {
					if (res.confirm) {
						uni.reLaunch({ url: '/pages/index/index' });
					}
				}
			});
		}
	},
	components: { QuizBirdList }
};
</script>

<style scoped>
/* 样式部分：Quiz问答页面的布局和样式，添加趣味性色彩和图标 */
.quiz-page { padding: 40rpx 30rpx; background: linear-gradient(135deg, #a8edea, #fed6e3); min-height: 100vh; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
.header { text-align: center; margin-bottom: 40rpx; padding-top: 20rpx; }
.title { font-size: 48rpx; font-weight: 800; color: #2d3436; text-shadow: 2rpx 2rpx 4rpx rgba(255,255,255,0.6); }
.score-display { font-size: 32rpx; color: #e17055; font-weight: bold; margin-top: 15rpx; background: rgba(255,255,255,0.7); display: inline-block; padding: 10rpx 30rpx; border-radius: 40rpx; box-shadow: 0 4rpx 10rpx rgba(0,0,0,0.05); }

.question { font-size: 36rpx; font-weight: 600; line-height: 1.5; margin-bottom: 40rpx; color: #2d3436; background: rgba(255,255,255,0.85); padding: 40rpx 30rpx; border-radius: 24rpx; box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.05); border-left: 10rpx solid #74b9ff; }
.options { display: flex; flex-direction: column; gap: 24rpx; margin-bottom: 30rpx; }
.option-btn { width: 100%; background: #ffffff; color: #2d3436; border-radius: 20rpx; padding: 24rpx 30rpx; font-size: 32rpx; font-weight: 500; box-shadow: 0 6rpx 12rpx rgba(0,0,0,0.04); transition: all 0.2s ease; border: 2rpx solid transparent; text-align: left; }
.option-btn:active { transform: scale(0.98); background: #fdfbfb; }

.answer { margin-top: 20rpx; margin-bottom: 30rpx; padding: 20rpx; border-radius: 16rpx; text-align: center; font-weight: bold; font-size: 32rpx; animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-10rpx); } to { opacity: 1; transform: translateY(0); } }
.correct { color: #00b894; background: #e8f8f5; border: 2rpx solid #c8e6c9; display: block; padding: 10rpx; border-radius: 12rpx; }
.wrong { color: #d63031; background: #fdedec; border: 2rpx solid #fadbd8; display: block; padding: 10rpx; border-radius: 12rpx; }

.next-btn { background: #0984e3; color: #fff; border-radius: 20rpx; padding: 24rpx 0; font-size: 32rpx; font-weight: bold; box-shadow: 0 8rpx 15rpx rgba(9,132,227,0.3); margin-top: 10rpx; }

.finish { text-align: center; margin-top: 80rpx; background: rgba(255,255,255,0.9); padding: 60rpx 40rpx; border-radius: 30rpx; box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.08); }
.finish-text { color: #2d3436; font-size: 40rpx; font-weight: 800; margin-bottom: 40rpx; display: block; }
.complete-btn { background: #ff7675; color: #fff; border-radius: 40rpx; padding: 20rpx 60rpx; font-size: 32rpx; font-weight: bold; box-shadow: 0 10rpx 20rpx rgba(255,118,117,0.4); animation: pulse 2s infinite; margin-bottom: 30rpx; }
.play-again-btn { background: #74b9ff; color: #fff; border-radius: 40rpx; padding: 20rpx 60rpx; font-size: 32rpx; font-weight: bold; margin-top: 10rpx; }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }

.result { background: rgba(255,255,255,0.95); border-radius: 30rpx; padding: 40rpx; margin-top: 30rpx; box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.1); }
.result-header { text-align: center; margin-bottom: 30rpx; border-bottom: 2rpx dashed #dfe6e9; padding-bottom: 20rpx; }
.result-title { font-size: 44rpx; font-weight: 800; color: #2d3436; }
.final-score { font-size: 36rpx; font-weight: bold; color: #00b894; margin-top: 16rpx; display: block; }

.history-section { margin-top: 30rpx; }
.history-title { font-size: 32rpx; font-weight: bold; color: #2d3436; margin-bottom: 20rpx; display: block; border-left: 8rpx solid #ff7675; padding-left: 16rpx; }
.history-list { max-height: 400rpx; overflow-y: auto; padding-right: 10rpx; }
.history-item { display: flex; justify-content: space-between; align-items: flex-start; padding: 20rpx; background: #f8f9fa; border-radius: 16rpx; margin-bottom: 16rpx; border-left: 6rpx solid #74b9ff; }
.history-q { font-size: 26rpx; color: #333; flex: 1; line-height: 1.4; padding-right: 20rpx; }
.correct-icon { font-size: 32rpx; }
.wrong-icon { font-size: 32rpx; }

.retry-btn { background: #00cec9; color: #fff; border-radius: 20rpx; padding: 24rpx 0; font-size: 32rpx; font-weight: bold; margin-top: 30rpx; box-shadow: 0 8rpx 15rpx rgba(0,206,201,0.3); }
.exit-btn { background: #ff7675; color: #fff; border-radius: 20rpx; padding: 24rpx 0; font-size: 32rpx; font-weight: bold; margin-top: 24rpx; box-shadow: 0 8rpx 15rpx rgba(255,118,117,0.3); }

.quiz-history { margin-top: 40rpx; padding: 30rpx; background: rgba(255,255,255,0.85); border-radius: 24rpx; box-shadow: 0 6rpx 15rpx rgba(0,0,0,0.05); }
.history-record { font-size: 26rpx; color: #636e72; padding: 16rpx 0; border-bottom: 2rpx dashed #dfe6e9; display: flex; justify-content: space-between; }
.quiz-bird-list-section { margin: 40rpx 0; }
</style>

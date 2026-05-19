<!-- App.vue: 应用的根组件，处理应用级生命周期事件，如启动、显示、隐藏，并检查用户登录状态 -->
<script>
	// 脚本部分：应用生命周期管理，包括登录检查
	export default {
		onLaunch: function() {
			console.log('App Launch')
			const apiBase = uni.getStorageSync('api_base_url');
			if (!apiBase) {
				uni.showModal({
					title: '服务未配置',
					content: '请先配置后端服务地址（扫描二维码或手动输入）。',
					success: (res) => {
						if (res.confirm) {
							uni.navigateTo({ url: '/pages/server_config' });
						}
					}
				});
			}
			// 检查是否已登录，未登录则跳转登录页
			const user = uni.getStorageSync('user_info');
			if (!user) {
				uni.reLaunch({ url: '/pages/login' });
			}
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/* 样式部分：每个页面公共CSS样式 */
</style>

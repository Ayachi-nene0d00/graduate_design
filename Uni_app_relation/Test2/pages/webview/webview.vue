<!-- webview.vue: WebView页面，用于在应用内显示外部网页，如搜索结果或百科页面 -->
<template>
	<view>
		<web-view :src="url"></web-view>
	</view>
</template>

<script>
// 脚本部分：接收URL参数并加载网页
export default {
	data() {
		return { url: '' };
	},
	onLoad(options) {
		// 接收并解码 URL
		if (options.url) {
			this.url = decodeURIComponent(options.url);
		}
	}
};
</script>
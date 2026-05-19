const DEFAULT_BASE_URL = 'http://192.168.1.103:8000';

function normalizeBaseUrl(url) {
	if (!url) return DEFAULT_BASE_URL;
	return url.endsWith('/') ? url.slice(0, -1) : url;
}

export function getBaseUrl() {
	const stored = uni.getStorageSync('api_base_url');
	return normalizeBaseUrl(stored || DEFAULT_BASE_URL);
}

export function setBaseUrl(url) {
	const normalized = normalizeBaseUrl(url);
	uni.setStorageSync('api_base_url', normalized);
	return normalized;
}

export function requestApi({ path, method = 'GET', data, header, timeout = 10000 }) {
	return uni.request({
		url: `${getBaseUrl()}${path}`,
		method,
		data,
		header,
		timeout
	});
}

export function uploadApi({ path, filePath, name = 'file', formData, timeout = 20000 }) {
	return new Promise((resolve, reject) => {
		uni.uploadFile({
			url: `${getBaseUrl()}${path}`,
			filePath,
			name,
			formData,
			timeout,
			success: resolve,
			fail: reject
		});
	});
}


const NAME_MAP_KEY = 'bird_name_local_map_v1';

function containsChinese(text) {
	return /[\u4e00-\u9fa5]/.test(text || '');
}

function normalizeCompareName(name) {
	return (name || '')
		.toString()
		.trim()
		.toLowerCase()
		.replace(/^[0-9]{1,3}[._\s-]*/, '')
		.replace(/[_-]+/g, ' ')
		.replace(/\s+/g, ' ')
		.replace(/[^\w\s.]/g, '')
		.trim();
}

function buildCandidateKeywords(rawName) {
	const raw = (rawName || '').toString().trim();
	if (!raw) return [];
	const noPrefix = raw.includes('.') ? raw.split('.').slice(1).join('.') : raw;
	const normalized = noPrefix.replace(/_/g, ' ').trim();
	const underscored = noPrefix.replace(/\s+/g, '_').trim();
	const compact = noPrefix.replace(/[.\s_-]+/g, '').trim();
	const candidates = [raw, noPrefix, normalized, underscored, compact];
	const seen = new Set();
	return candidates.filter((item) => {
		const key = normalizeCompareName(item);
		if (!key || seen.has(key)) return false;
		seen.add(key);
		return true;
	});
}

function readNameMap() {
	try {
		return uni.getStorageSync(NAME_MAP_KEY) || {};
	} catch (e) {
		return {};
	}
}

function writeNameMap(map) {
	try {
		uni.setStorageSync(NAME_MAP_KEY, map);
	} catch (e) {}
}

function parseBirdListResponse(res) {
	const response = res && res.data ? res : (Array.isArray(res) ? (res[1] || {}) : {});
	const payload = response.data || {};
	return payload.code === 0 && Array.isArray(payload.data) ? payload.data : [];
}

function findChineseName(birdList, keywords) {
	if (!Array.isArray(birdList) || !birdList.length) return '';
	const keySet = new Set(keywords.map(normalizeCompareName).filter(Boolean));
	let fallback = '';
	for (const bird of birdList) {
		const cnName = (bird && bird.name ? String(bird.name) : '').trim();
		if (!cnName) continue;
		if (!fallback && containsChinese(cnName)) fallback = cnName;
		if (!containsChinese(cnName)) continue;
		const englishName = normalizeCompareName(bird.english_name || '');
		const nameNorm = normalizeCompareName(cnName);
		if ((englishName && keySet.has(englishName)) || (nameNorm && keySet.has(nameNorm))) {
			return cnName;
		}
	}
	return fallback;
}

export function formatBirdDisplayName(name) {
	const raw = (name || '').toString().trim();
	if (!raw) return '未知鸟类';
	if (containsChinese(raw)) return raw;
	const noPrefix = raw.includes('.') ? raw.split('.').slice(1).join('.') : raw;
	return noPrefix.replace(/_/g, ' ').trim() || raw;
}

export async function localizeBirdName(name, requestApiFn) {
	const raw = (name || '').toString().trim();
	if (!raw) return '未知鸟类';
	if (containsChinese(raw) || typeof requestApiFn !== 'function') {
		return formatBirdDisplayName(raw);
	}

	const nameMap = readNameMap();
	if (nameMap[raw]) {
		const cached = formatBirdDisplayName(nameMap[raw]);
		if (containsChinese(cached)) return cached;
	}

	const keywords = buildCandidateKeywords(raw);
	for (const keyword of keywords) {
		try {
			const res = await requestApiFn({
				path: `/api/bird?page=1&page_size=20&keyword=${encodeURIComponent(keyword)}`,
				method: 'GET',
				timeout: 5000
			});
			const birdList = parseBirdListResponse(res);
			const cnName = findChineseName(birdList, keywords);
			if (cnName) {
				nameMap[raw] = cnName;
				writeNameMap(nameMap);
				return cnName;
			}
		} catch (e) {
			console.warn('鸟名本地化查询失败:', e);
		}
	}

	const fallback = formatBirdDisplayName(raw);
	nameMap[raw] = fallback;
	writeNameMap(nameMap);
	return fallback;
}

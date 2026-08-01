<!-- index.vue: 主页，包含搜索栏、GPS推荐、测验、模式选择、图片上传、识别结果、快速导航等功能 -->
<template>
  <view class="page">
    <view class="top-bar">
      <view class="brand" @click="goToSearch">
        <image class="brand-logo" src="/static/pk.png" mode="aspectFit" />
        <text class="brand-name">趣识鸟</text>
      </view>
    </view>

    <view class="search-box" @click="goToSearch">
      <text class="search-icon">🔍</text>
      <text class="search-placeholder">搜索鸟类中、英、拉丁名</text>
    </view>

    <view class="history-title" @click="goToSearch">
      <text class="history-icon">≡</text>
      <text class="history-text">鸟类知识检索</text>
    </view>
    <view v-if="localSearchHistory.length" class="history-tag-list">
      <view
        class="history-chip"
        v-for="(item, index) in (showAllSearchHistory ? localSearchHistory : localSearchHistory.slice(0, 4))"
        :key="index"
        @click="openSearchItem(item)"
      >
        {{ item }}
      </view>
      <view
        v-if="localSearchHistory.length > 4"
        class="history-chip history-more"
        @click="toggleSearchHistory"
      >
        {{ showAllSearchHistory ? '收起' : '...' }}
      </view>
    </view>
    <view v-else class="history-empty" @click="goToSearch">暂无历史搜索</view>

    <view class="shortcut-row">
      <view class="shortcut-item" @click="goToQuiz">
        <view class="shortcut-icon">🎯</view>
        <text class="shortcut-label">趣味问答</text>
      </view>
      <view class="shortcut-item" @click="goToEncyclopedia">
        <view class="shortcut-icon">📚</view>
        <text class="shortcut-label">鸟类科普库</text>
      </view>
      <view class="shortcut-item" @click="goToCompare">
        <view class="shortcut-icon">🆚</view>
        <text class="shortcut-label">鸟界PK</text>
      </view>
    </view>

    <view class="recommend-card" @click="goToGPS">
      <view class="recommend-img-wrap">
        <image class="recommend-img" :src="recommendImg" mode="aspectFit" @error="handleRecommendImageError" />
      </view>
      <view class="recommend-overlay">
        <text class="recommend-name">{{ formatName(dailyBird) || '今日推荐' }}</text>
        <text class="recommend-sub">今日推荐</text>
      </view>
    </view>

    <view class="recent-header">
      <view class="recent-left">
        <text class="recent-icon">⟳</text>
        <text class="recent-title">最近识别</text>
      </view>
      <text class="recent-more" @click="goToHistory">查看全部 ></text>
    </view>

    <view v-if="historyList.length" class="recent-list">
      <view
        class="recent-item"
        v-for="(item, index) in historyList.slice(0, 5)"
        :key="index"
        @click="openHistoryItem(item)"
      >
        <view class="recent-img-wrap">
          <image class="recent-img" :src="item.img" mode="aspectFit" />
        </view>
        <view class="recent-info">
          <text class="recent-name">{{ formatName(item.name) }}</text>
          <text class="recent-conf">匹配度 {{ (item.conf * 100).toFixed(1) }}%</text>
        </view>
      </view>
    </view>
    <view v-else class="recent-empty">
      点击下方按钮，开始图片/声音识别鸟类~
    </view>

    <view class="bottom-bar">
      <view class="bottom-item" @click="goHome">
        <view class="bottom-icon">🏠</view>
        <text class="bottom-text">首页</text>
      </view>
      <view class="recognize-btn" @click="openRecognizeMenu">
        <view class="recognize-icon">📷</view>
        <text class="recognize-text">识别</text>
      </view>
      <view class="bottom-item" @click="goToProfile">
        <view class="bottom-icon">👤</view>
        <text class="bottom-text">我的</text>
      </view>
    </view>
  </view>
</template>

<script>
// 脚本部分：主页逻辑，包括图片选择、ONNX推理、结果处理、导航跳转等
import { uploadApi, requestApi, getBaseUrl } from '@/common/api';
import { formatBirdDisplayName, localizeBirdName } from '@/common/bird_name_localizer';
const BIRD_PLACEHOLDER = 'https://img.haoma.com/bird_placeholder.jpg';
const DEFAULT_PROVINCE = '四川';
export default {
	data() {
		return {
			imgUrl: '',
			loading: false,
			dailyBird: '',
			result: null,
      recommendImg: BIRD_PLACEHOLDER,
      historyList: [],
      localSearchHistory: [],
      showAllSearchHistory: false,
      latestHistoryName: '',
			birdNames: [
  "001.Black_footed_Albatross",
  "002.Laysan_Albatross",
  "003.Sooty_Albatross",
  "004.Groove_billed_Ani",
  "005.Crested_Auklet",
  "006.Least_Auklet",
  "007.Parakeet_Auklet",
  "008.Rhinoceros_Auklet",
  "009.Brewer_Blackbird",
  "010.Red_winged_Blackbird",
  "011.Rusty_Blackbird",
  "012.Yellow_headed_Blackbird",
  "013.Bobolink",
  "014.Indigo_Bunting",
  "015.Lazuli_Bunting",
  "016.Painted_Bunting",
  "017.Cardinal",
  "018.Spotted_Catbird",
  "019.Gray_Catbird",
  "020.Yellow_breasted_Chat",
  "021.Eastern_Towhee",
  "022.Chuck_will_Widow",
  "023.Brandt_Cormorant",
  "024.Red_faced_Cormorant",
  "025.Pelagic_Cormorant",
  "026.Bronzed_Cowbird",
  "027.Shiny_Cowbird",
  "028.Brown_Creeper",
  "029.American_Crow",
  "030.Fish_Crow",
  "031.Black_billed_Cuckoo",
  "032.Mangrove_Cuckoo",
  "033.Yellow_billed_Cuckoo",
  "034.Gray_crowned_Rosy_Finch",
  "035.Purple_Finch",
  "036.Northern_Flicker",
  "037.Acadian_Flycatcher",
  "038.Great_Crested_Flycatcher",
  "039.Least_Flycatcher",
  "040.Olive_sided_Flycatcher",
  "041.Scissor_tailed_Flycatcher",
  "042.Vermilion_Flycatcher",
  "043.Yellow_bellied_Flycatcher",
  "044.Frigatebird",
  "045.Northern_Fulmar",
  "046.Gadwall",
  "047.American_Goldfinch",
  "048.European_Goldfinch",
  "049.Boat_tailed_Grackle",
  "050.Eared_Grebe",
  "051.Horned_Grebe",
  "052.Pied_billed_Grebe",
  "053.Western_Grebe",
  "054.Blue_Grosbeak",
  "055.Evening_Grosbeak",
  "056.Pine_Grosbeak",
  "057.Rose_breasted_Grosbeak",
  "058.Pigeon_Guillemot",
  "059.California_Gull",
  "060.Glaucous_winged_Gull",
  "061.Heermann_Gull",
  "062.Herring_Gull",
  "063.Ivory_Gull",
  "064.Ring_billed_Gull",
  "065.Slaty_backed_Gull",
  "066.Western_Gull",
  "067.Anna_Hummingbird",
  "068.Ruby_throated_Hummingbird",
  "069.Rufous_Hummingbird",
  "070.Green_Violetear",
  "071.Long_tailed_Jaeger",
  "072.Pomarine_Jaeger",
  "073.Blue_Jay",
  "074.Florida_Jay",
  "075.Green_Jay",
  "076.Dark_eyed_Junco",
  "077.Tropical_Kingbird",
  "078.Gray_Kingbird",
  "079.Belted_Kingfisher",
  "080.Green_Kingfisher",
  "081.Pied_Kingfisher",
  "082.Ringed_Kingfisher",
  "083.White_breasted_Kingfisher",
  "084.Red_legged_Kittiwake",
  "085.Horned_Lark",
  "086.Pacific_Loon",
  "087.Mallard",
  "088.Western_Meadowlark",
  "089.Hooded_Merganser",
  "090.Red_breasted_Merganser",
  "091.Mockingbird",
  "092.Nighthawk",
  "093.Clark_Nutcracker",
  "094.White_breasted_Nuthatch",
  "095.Baltimore_Oriole",
  "096.Hooded_Oriole",
  "097.Orchard_Oriole",
  "098.Scott_Oriole",
  "099.Ovenbird",
  "100.Brown_Pelican",
  "101.White_Pelican",
  "102.Western_Wood_Pewee",
  "103.Sayornis",
  "104.American_Pipit",
  "105.Whip_poor_Will",
  "106.Horned_Puffin",
  "107.Common_Raven",
  "108.White_necked_Raven",
  "109.American_Redstart",
  "110.Geococcyx",
  "111.Loggerhead_Shrike",
  "112.Great_Grey_Shrike",
  "113.Baird_Sparrow",
  "114.Black_throated_Sparrow",
  "115.Brewer_Sparrow",
  "116.Chipping_Sparrow",
  "117.Clay_colored_Sparrow",
  "118.House_Sparrow",
  "119.Field_Sparrow",
  "120.Fox_Sparrow",
  "121.Grasshopper_Sparrow",
  "122.Harris_Sparrow",
  "123.Henslow_Sparrow",
  "124.Le_Conte_Sparrow",
  "125.Lincoln_Sparrow",
  "126.Nelson_Sharp_tailed_Sparrow",
  "127.Savannah_Sparrow",
  "128.Seaside_Sparrow",
  "129.Song_Sparrow",
  "130.Tree_Sparrow",
  "131.Vesper_Sparrow",
  "132.White_crowned_Sparrow",
  "133.White_throated_Sparrow",
  "134.Cape_Glossy_Starling",
  "135.Bank_Swallow",
  "136.Barn_Swallow",
  "137.Cliff_Swallow",
  "138.Tree_Swallow",
  "139.Scarlet_Tanager",
  "140.Summer_Tanager",
  "141.Artic_Tern",
  "142.Black_Tern",
  "143.Caspian_Tern",
  "144.Common_Tern",
  "145.Elegant_Tern",
  "146.Forsters_Tern",
  "147.Least_Tern",
  "148.Green_tailed_Towhee",
  "149.Brown_Thrasher",
  "150.Sage_Thrasher",
  "151.Black_capped_Vireo",
  "152.Blue_headed_Vireo",
  "153.Philadelphia_Vireo",
  "154.Red_eyed_Vireo",
  "155.Warbling_Vireo",
  "156.White_eyed_Vireo",
  "157.Yellow_throated_Vireo",
  "158.Bay_breasted_Warbler",
  "159.Black_and_white_Warbler",
  "160.Black_throated_Blue_Warbler",
  "161.Blue_winged_Warbler",
  "162.Canada_Warbler",
  "163.Cape_May_Warbler",
  "164.Cerulean_Warbler",
  "165.Chestnut_sided_Warbler",
  "166.Golden_winged_Warbler",
  "167.Hooded_Warbler",
  "168.Kentucky_Warbler",
  "169.Magnolia_Warbler",
  "170.Mourning_Warbler",
  "171.Myrtle_Warbler",
  "172.Nashville_Warbler",
  "173.Orange_crowned_Warbler",
  "174.Palm_Warbler",
  "175.Pine_Warbler",
  "176.Prairie_Warbler",
  "177.Prothonotary_Warbler",
  "178.Swainson_Warbler",
  "179.Tennessee_Warbler",
  "180.Wilson_Warbler",
  "181.Worm_eating_Warbler",
  "182.Yellow_Warbler",
  "183.Northern_Waterthrush",
  "184.Louisiana_Waterthrush",
  "185.Bohemian_Waxwing",
  "186.Cedar_Waxwing",
  "187.American_Three_toed_Woodpecker",
  "188.Pileated_Woodpecker",
  "189.Red_bellied_Woodpecker",
  "190.Red_cockaded_Woodpecker",
  "191.Red_headed_Woodpecker",
  "192.Downy_Woodpecker",
  "193.Bewick_Wren",
  "194.Cactus_Wren",
  "195.Carolina_Wren",
  "196.House_Wren",
  "197.Marsh_Wren",
  "198.Rock_Wren",
  "199.Winter_Wren",
  "200.Common_Yellowthroat",
  "201.Abroscopus_schisticeps",
  "202.Accipiter_trivirgatus",
  "203.Acridotheres_cristatellus",
  "204.Acrocephalus_arundinaceus",
  "205.Actinodura_morrisoniana",
  "206.Aegithalos_caudatus",
  "207.Aegithina_lafresnayei",
  "208.Aethopyga_christinae",
  "209.Aethopyga_gouldiae",
  "210.Aethopyga_siparaja",
  "211.Alauda_leucoptera",
  "212.Alophoixus_flaveolus",
  "213.Amaurornis_phoenicurus",
  "214.Anas_platyrhynchos",
  "215.Anas_zonorhyncha",
  "216.Anser_albifrons",
  "217.Anser_anser",
  "218.Anser_cygnoides",
  "219.Anser_fabalis",
  "220.Anser_serrirostris",
  "221.Anthracoceros_albirostris",
  "222.Anthus_roseatus",
  "223.Anthus_rubescens",
  "224.Antigone_vipio",
  "225.Aquila_chrysaetos",
  "226.Arborophila_gingica",
  "227.Ardea_alba",
  "228.Ardea_cinerea",
  "229.Ardea_purpurea",
  "230.Ardenna_grisea",
  "231.Ardeola_bacchus",
  "232.Asio_otus",
  "233.Athene_noctua",
  "234.Aviceda_leuphotes",
  "235.Branta_hutchinsii",
  "236.Bubo_bubo",
  "237.Bucanetes_mongolicus",
  "238.Calamornis_heudei",
  "239.Calandrella_brachydactyla",
  "240.Calidris_alba",
  "241.Calidris_subminuta",
  "242.Carpodacus_rubicilla",
  "243.Carpodacus_sipahi",
  "244.Carpodacus_vinaceus",
  "245.Cephalopyrus_flammiceps",
  "246.Certhia_himalayana",
  "247.Cettia_brunnifrons",
  "248.Charadrius_asiaticus",
  "249.Charadrius_placidus",
  "250.Chroicocephalus_ridibundus",
  "251.Chrysocolaptes_guttacristatus",
  "252.Chrysophlegma_flavinucha",
  "253.Ciconia_boyciana",
  "254.Ciconia_ciconia",
  "255.Cinclidium_frontale",
  "256.Cinnyris_asiaticus",
  "257.Circus_macrourus",
  "258.Cochoa_viridis",
  "259.Columba_rupestris",
  "260.Corvus_corone",
  "261.Crossoptilon_auritum",
  "262.Cygnus_columbianus",
  "263.Cygnus_cygnus",
  "264.Cyornis_poliogenys",
  "265.Dicaeum_agile",
  "266.Dicaeum_cruentatum",
  "267.Egretta_garzetta",
  "268.Elachura_formosa",
  "269.Falco_cherrug",
  "270.Ficedula_elisae",
  "271.Ficedula_erithacus",
  "272.Ficedula_tricolor",
  "273.Fulica_atra",
  "274.Fulvetta_formosana",
  "275.Fulvetta_ludlowi",
  "276.Gallicrex_cinerea",
  "277.Gallinula_chloropus",
  "278.Gampsorhynchus_torquatus",
  "279.Gavia_adamsii",
  "280.Glaucidium_cuculoides",
  "281.Gracula_religiosa",
  "282.Grus_grus",
  "283.Grus_monacha",
  "284.Haematopus_ostralegus",
  "285.Helopsaltes_certhiola",
  "286.Helopsaltes_fasciolatus",
  "287.Hemixos_flavala",
  "288.Hierococcyx_varius",
  "289.Himantopus_himantopus",
  "290.Hirundapus_giganteus",
  "291.Hirundo_rustica",
  "292.Horornis_fortipes",
  "293.Ichthyaetus_ichthyaetus",
  "294.Iduna_caligata",
  "295.Lalage_melaschistos",
  "296.Lanius_borealis",
  "297.Lanius_schach",
  "298.Larus_crassirostris",
  "299.Larus_fuscus",
  "300.Larus_schistisagus",
  "301.Larvivora_akahige",
  "302.Leptopoecile_sophiae",
  "303.Leucosticte_nemoricola",
  "304.Lewinia_striata",
  "305.Limnodromus_scolopaceus",
  "306.Limnodromus_semipalmatus",
  "307.Limosa_limosa",
  "308.Locustella_lanceolata",
  "309.Lophophorus_sclateri",
  "310.Lyncornis_macrotis",
  "311.Mareca_penelope",
  "312.Melanochlora_sultanea",
  "313.Melanocorypha_mongolica",
  "314.Mergellus_albellus",
  "315.Mergus_serrator",
  "316.Metopidius_indicus",
  "317.Microcarbo_pygmaeus",
  "318.Monticola_solitarius",
  "319.Montifringilla_henrici",
  "320.Motacilla_citreola",
  "321.Myophonus_insularis",
  "322.Neophron_percnopterus",
  "323.Netta_rufina",
  "324.Niltava_davidi",
  "325.Nipponia_nippon",
  "326.Nycticorax_nycticorax",
  "327.Oceanites_oceanicus",
  "328.Oxyura_leucocephala",
  "329.Parus_major",
  "330.Parus_monticolus",
  "331.Passer_domesticus",
  "332.Passer_montanus",
  "333.Pavo_cristatus",
  "334.Pavo_muticus",
  "335.Pericrocotus_divaricatus",
  "336.Periparus_ater",
  "337.Perisoreus_infaustus",
  "338.Phalacrocorax_capillatus",
  "339.Phalacrocorax_carbo",
  "340.Phalaropus_lobatus",
  "341.Phoenicurus_fuliginosus",
  "342.Phylloscopus_affinis",
  "343.Phylloscopus_burkii",
  "344.Phylloscopus_goodsoni",
  "345.Phylloscopus_trochiloides",
  "346.Phylloscopus_yunnanensis",
  "347.Pica_bottanensis",
  "348.Pica_serica",
  "349.Picus_vittatus",
  "350.Platalea_leucorodia",
  "351.Platalea_minor",
  "352.Pnoepyga_mutica",
  "353.Podiceps_auritus",
  "354.Podiceps_cristatus",
  "355.Poliolimnas_cinereus",
  "356.Pomatorhinus_ferruginosus",
  "357.Prunella_fulvescens",
  "358.Psilopogon_haemacephalus",
  "359.Psittacula_derbiana",
  "360.Pterodroma_hypoleuca",
  "361.Pterorhinus_poecilorhynchus",
  "362.Pterorhinus_sannio",
  "363.Pycnonotus_goiavier",
  "364.Saxicola_jerdoni",
  "365.Sibirionetta_formosa",
  "366.Sinosuthora_brunnea",
  "367.Spatula_clypeata",
  "368.Spelaeornis_troglodytoides",
  "369.Spizixos_canifrons",
  "370.Stachyris_nonggangensis",
  "371.Staphida_castaniceps",
  "372.Sterna_hirundo",
  "373.Strix_nivicolum",
  "374.Suthora_nipalensis",
  "375.Tadorna_ferruginea",
  "376.Tadorna_tadorna",
  "377.Taenioptynx_brodiei",
  "378.Tarsiger_indicus",
  "379.Tephrodornis_virgatus",
  "380.Thalasseus_bergii",
  "381.Thalasseus_bernsteini",
  "382.Tragopan_satyra",
  "383.Tringa_erythropus",
  "384.Tringa_flavipes",
  "385.Tringa_ochropus",
  "386.Trochalopteron_erythrocephalum",
  "387.Trochalopteron_imbricatum",
  "388.Trochalopteron_variegatum",
  "389.Turdus_eunomus",
  "390.Turdus_naumanni",
  "391.Turdus_niveiceps",
  "392.Turdus_obscurus",
  "393.Turdus_rubrocanus",
  "394.Urocynchramus_pylzowi",
  "395.Urosphena_squameiceps",
  "396.Yuhina_nigrimenta",
  "397.Zoothera_aurea",
  "398.Zoothera_mollissima",
  "399.Zosterops_erythropleurus",
  "400.Zosterops_meyeni"
]
		};
	},
	onLoad() {
    this.getGPSRecommend();
	},
  onShow() {
    this.loadHistory();
    this.loadSearchHistory();
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
      this.latestHistoryName = this.historyList.length ? this.historyList[0].name : '';
    },
    loadSearchHistory() {
      this.localSearchHistory = uni.getStorageSync('search_history') || [];
      if (this.localSearchHistory.length <= 4) {
        this.showAllSearchHistory = false;
      }
    },
    toggleSearchHistory() {
      this.showAllSearchHistory = !this.showAllSearchHistory;
    },
    async openSearchItem(name) {
      if (!name) return;
      try {
        const res = await requestApi({
          path: `/api/bird?page=1&page_size=1&keyword=${encodeURIComponent(name)}`,
          method: 'GET'
        });
        const response = res.data ? res : (res[1] || {});
        const list = response.data && response.data.code === 0 ? response.data.data : [];
        if (list && list.length) {
          uni.navigateTo({
            url: `/pages/encyclopedia_detail?bird_id=${list[0].bird_id}`
          });
          return;
        }
        uni.showToast({ title: '未找到该鸟类', icon: 'none' });
      } catch (e) {
        uni.showToast({ title: '查询失败，请稍后再试', icon: 'none' });
      }
    },
    openRecognizeMenu() {
      uni.showActionSheet({
        itemList: ['相册', '拍照'],
        success: (res) => {
          if (res.tapIndex === 0) {
            this.chooseFromAlbum(true);
          } else if (res.tapIndex === 1) {
            this.chooseFromCamera(true);
          }
        }
      });
    },
		async getGPSRecommend() {
			try {
				// 与 gps.vue 默认省份保持一致，未定位时回退到默认省份
				const city = uni.getStorageSync('gps_city') || DEFAULT_PROVINCE;
				const res = await requestApi({
					path: `/api/recommend?city=${encodeURIComponent(city)}`,
					method: 'GET',
					timeout: 5000
				});
				// 兼容 requestApi 在不同平台返回对象或 [err, response] 两种结构
				const response = res.data ? res : (res[1] || {});
				if (response.statusCode === 200 && response.data && response.data.code === 0) {
					const firstBird = (response.data.data || [])[0];
					if (firstBird) {
						this.dailyBird = firstBird.name || '';
						this.recommendImg = this.normalizeImageUrl(firstBird.image_url);
						return;
					}
				}
			} catch (e) {
				console.warn('Get GPS recommendation failed:', e);
			}
			this.dailyBird = '';
			this.recommendImg = BIRD_PLACEHOLDER;
		},
		normalizeImageUrl(url) {
			if (!url) return BIRD_PLACEHOLDER;
			if (url.startsWith('http')) return url;
			const baseUrl = getBaseUrl().replace(/\/$/, '');
			return baseUrl + (url.startsWith('/') ? url : '/' + url);
		},
    handleRecommendImageError() {
      this.recommendImg = BIRD_PLACEHOLDER;
    },
		formatName(name) {
			return formatBirdDisplayName(name);
		},
		// 直接跳转鸟网首页
		goBirdNet() {
			uni.navigateTo({
				url: `/pages/webview/webview?url=${encodeURIComponent('http://www.birdnet.cn/')}`
			});
		},
		// 深度搜索保持使用搜索引擎，帮助确认细节
		goDeepSearch(name) {
			const url = `https://www.bing.com/search?q=${encodeURIComponent(name + ' 鸟类特征')}`;
			uni.navigateTo({
				url: `/pages/webview/webview?url=${encodeURIComponent(url)}`
			});
		},
    chooseImage(sourceType, autoIdentify = false) {
      const types = sourceType ? [sourceType] : ['album', 'camera'];
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: types,
        success: (res) => {
          this.imgUrl = res.tempFilePaths[0];
          this.result = null;
          if (autoIdentify) {
            this.handleIdentify();
          }
        }
      });
    },
    chooseFromAlbum(autoIdentify = false) {
      this.chooseImage('album', autoIdentify);
    },
    chooseFromCamera(autoIdentify = false) {
      this.chooseImage('camera', autoIdentify);
    },
		handleIdentify() {
			if (!this.imgUrl) return uni.showToast({ title: '请先选取照片', icon: 'none' });
			this.runInference();
		},
		async runInference() {
			this.loading = true;
			uni.showLoading({ title: '正在识别...' });

      try {
        const uploadFileRes = await uploadApi({
          path: '/predict',
          filePath: this.imgUrl,
          name: 'file'
        });
					uni.hideLoading();
					this.loading = false;

					try {
						let resData = JSON.parse(uploadFileRes.data);
						if (resData.code === 0) {
							const localizedName = await localizeBirdName(resData.bird_name, requestApi);
							this.result = { name: localizedName, conf: resData.confidence };

							uni.vibrateShort();
							await this.saveToHistory(this.result.name, this.result.conf, this.imgUrl);

							uni.navigateTo({
								url: `/pages/share/share?name=${this.result.name}&conf=${this.result.conf}&img=${encodeURIComponent(this.imgUrl)}`
							});
						} else {
							uni.showToast({ title: `识别失败: ${resData.message}`, icon: 'none' });
						}
					} catch(e) {
						uni.showToast({ title: '数据解析失败', icon: 'none' });
					}
      } catch (err) {
        uni.hideLoading();
        this.loading = false;
        console.error("请求发送失败", err);
        uni.showModal({
          title: '网络连接失败',
          content: '请检查测试手机是否连接到与电脑同一个 Wi-Fi 网络，并确认服务地址配置正确。',
          showCancel: false
        });
      }
		},
		async persistImage(tempPath) {
      if (!tempPath || tempPath.startsWith('http') || tempPath.startsWith('data:image/')) {
        return tempPath;
      }
      // 优先保存到本地持久目录，确保重启后仍可用
      const savedPath = await new Promise((resolve) => {
        uni.saveFile({
          tempFilePath: tempPath,
          success: (res) => resolve(res.savedFilePath),
          fail: () => resolve('')
        });
      });
      if (savedPath) {
        return savedPath;
      }
      // saveFile 不可用时，降级为 base64 存储
      try {
        const fs = uni.getFileSystemManager && uni.getFileSystemManager();
        if (fs && fs.readFileSync) {
          const base64 = fs.readFileSync(tempPath, 'base64');
          return `data:image/jpeg;base64,${base64}`;
        }
      } catch (e) {
        // 保持静默，返回原路径
      }
      return tempPath;
    },
		async saveToHistory(name, conf, img) {
      const cachedImg = await this.persistImage(img);
			let history = uni.getStorageSync('bird_history') || [];
			history.unshift({ name, conf, img: cachedImg, time: new Date().toLocaleString() });
			uni.setStorageSync('bird_history', history.slice(0, 20));
      this.loadHistory();
		},
    openHistoryItem(item) {
      if (!item) return;
      uni.navigateTo({
        url: `/pages/share/share?name=${item.name}&conf=${item.conf}&img=${encodeURIComponent(item.img)}`
      });
    },
    goHome() {
      uni.pageScrollTo({ scrollTop: 0, duration: 200 });
    },
		goToSearch() { uni.navigateTo({ url: '/pages/search/search' }); },
    goToSearchWithKeyword(keyword) {
      uni.navigateTo({
        url: `/pages/search/search?keyword=${encodeURIComponent(keyword)}`
      });
    },
		goToHistory() { uni.navigateTo({ url: '/pages/history/history' }); },
		goToEncyclopedia() { uni.navigateTo({ url: '/pages/encyclopedia' }); },
		goToProfile() { uni.navigateTo({ url: '/pages/profile' }); },
		goToAIQA() { uni.navigateTo({ url: '/pages/aiqa' }); },
		goToGPS() { uni.navigateTo({ url: '/pages/gps' }); },
		goToQuiz() { uni.navigateTo({ url: '/pages/quiz' }); },
		goToCompare() { uni.navigateTo({ url: '/pages/compare' }); },
		openInstruction() {
			uni.showModal({ title: '提示', content: '上传鸟类照片后点击识别，即可获取品种名称并存储历史。', showCancel: false });
		},
		// --- ONNX 工具函数 ---
		async initOrt() {
			if (window.ort) return window.ort;
			return new Promise(r => {
				const s = document.createElement('script');
				s.src = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.14.0/dist/ort.min.js';
				s.onload = () => r(window.ort);
				document.head.appendChild(s);
			});
		},
		preprocess(url, size) {
			return new Promise(resolve => {
				const img = new Image(); img.src = url;
				img.onload = () => {
					const canvas = document.createElement('canvas');
					canvas.width = size; canvas.height = size;
					const ctx = canvas.getContext('2d');
					ctx.drawImage(img, 0, 0, size, size);
					const data = ctx.getImageData(0, 0, size, size).data;
					const [r, g, b] = [new Float32Array(size*size), new Float32Array(size*size), new Float32Array(size*size)];
					for (let i = 0; i < size * size; i++) {
						r[i] = (data[i*4]/255 - 0.485)/0.229;
						g[i] = (data[i*4+1]/255 - 0.456)/0.224;
						b[i] = (data[i*4+2]/255 - 0.406)/0.225;
					}
					const tensorData = new Float32Array(3*size*size);
					tensorData.set(r,0); tensorData.set(g,size*size); tensorData.set(b,2*size*size);
					resolve(new window.ort.Tensor('float32', tensorData, [1, 3, size, size]));
				}
			});
		},
		postProcess(logits) {
			const probs = Array.from(logits);
			let idx = 0, max = -Infinity;
			probs.forEach((p, i) => { if(p > max){ max = p; idx = i; } });
			return { name: this.birdNames[idx], conf: max };
		}
	}
};
</script>

<style scoped>
.page {
  background: #f8f8f8;
  min-height: 100vh;
  padding: 28rpx 28rpx 180rpx;
  box-sizing: border-box;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20rpx;
}
.brand {
  display: flex;
  align-items: center;
  gap: 14rpx;
}
.brand-logo { width: 54rpx; height: 54rpx; }
.brand-name { font-size: 38rpx; font-weight: 700; color: #111; }
.search-box {
  background: #fff;
  border-radius: 18rpx;
  padding: 18rpx 24rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 22rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.04);
}
.search-icon { font-size: 30rpx; color: #8b8b8b; }
.search-placeholder { font-size: 28rpx; color: #9aa0a6; }

.history-title { display: flex; align-items: center; gap: 12rpx; margin-bottom: 12rpx; }
.history-icon { font-size: 32rpx; }
.history-text { font-size: 30rpx; font-weight: 700; color: #111; }
.history-tag-list {
  display: flex;
  align-items: center;
  gap: 12rpx;
  flex-wrap: wrap;
  margin-bottom: 24rpx;
}
.history-chip {
  background: #f1f1f1;
  border-radius: 14rpx;
  padding: 10rpx 18rpx;
  font-size: 24rpx;
  color: #666;
}
.history-more {
  padding: 10rpx 22rpx;
}
.history-empty {
  font-size: 24rpx;
  color: #9aa0a6;
  margin-bottom: 24rpx;
}

.shortcut-row { display: flex; justify-content: space-between; gap: 16rpx; margin-bottom: 26rpx; }
.shortcut-item {
  flex: 1;
  background: #fff;
  border-radius: 18rpx;
  padding: 20rpx 0;
  text-align: center;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
}
.shortcut-icon { font-size: 34rpx; margin-bottom: 8rpx; }
.shortcut-label { font-size: 24rpx; color: #222; }

.recommend-card {
  width: 100%;
  height: 260rpx;
  border-radius: 20rpx;
  overflow: hidden;
  position: relative;
  margin-bottom: 26rpx;
  box-shadow: 0 10rpx 20rpx rgba(0,0,0,0.08);
}
.recommend-img-wrap {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.recommend-img { width: 100%; height: 100%; }
.recommend-overlay {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  padding: 18rpx 20rpx;
  background: linear-gradient(transparent, rgba(0,0,0,0.65));
}
.recommend-name { font-size: 32rpx; color: #fff; font-weight: 700; display: block; }
.recommend-sub { font-size: 22rpx; color: rgba(255,255,255,0.8); margin-top: 6rpx; display: block; }

.recent-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.recent-left { display: flex; align-items: center; gap: 10rpx; }
.recent-icon { font-size: 30rpx; }
.recent-title { font-size: 30rpx; font-weight: 700; color: #111; }
.recent-more { font-size: 24rpx; color: #777; }

.recent-list {
  background: #fff;
  border-radius: 18rpx;
  padding: 18rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}
.recent-item { display: flex; gap: 16rpx; align-items: center; }
.recent-img-wrap {
  width: 120rpx;
  height: 120rpx;
  border-radius: 16rpx;
  background: #f0f0f0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.recent-img { width: 100%; height: 100%; }
.recent-info { display: flex; flex-direction: column; }
.recent-name { font-size: 28rpx; color: #222; font-weight: 600; }
.recent-conf { font-size: 22rpx; color: #8c8c8c; margin-top: 6rpx; }
.recent-empty { font-size: 24rpx; color: #9aa0a6; padding: 24rpx 0; text-align: center; }

.bottom-bar {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background: #fff;
  padding: 20rpx 40rpx 32rpx;
  box-shadow: 0 -6rpx 20rpx rgba(0,0,0,0.08);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  box-sizing: border-box;
}
.bottom-item {
  flex: 1;
  text-align: center;
  color: #9aa0a6;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}
.bottom-icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: #fff;
  border: 2rpx solid #eee;
  font-size: 30rpx;
  line-height: 72rpx;
  text-align: center;
}
.bottom-text { font-size: 22rpx; color: #8a8f99; }
.recognize-btn {
  width: 160rpx;
  height: 160rpx;
  border-radius: 50%;
  background: #111;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10rpx 24rpx rgba(0,0,0,0.2);
}
.recognize-icon { font-size: 40rpx; margin-bottom: 6rpx; }
.recognize-text { font-size: 28rpx; font-weight: 700; }
</style>

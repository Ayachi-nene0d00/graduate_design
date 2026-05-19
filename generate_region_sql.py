import os
import glob
import random
from ultralytics import YOLO

BASE_DIR = r"F:\Python-program\111"

def main():
    # 1. 自动寻找最新模型
    search_pattern = os.path.join(BASE_DIR, "runs", "**", "best.pt")
    found_files = glob.glob(search_pattern, recursive=True)
    
    if not found_files:
        print("❌ 未找到 best.pt 模型！")
        return
        
    found_files.sort(key=os.path.getmtime, reverse=True)
    pt_path = found_files[0]
    print(f"✅ 加载模型：{pt_path}")

    # 2. 读取模型中的英文类名
    model = YOLO(pt_path)
    names_dict = model.names

    # 3. 准备生成的 SQL 列表
    # 增加了 country, province, city 字段，province 映射到其首府/省会
    prov_city_map = {
        "四川": "成都", "云南": "昆明", "贵州": "贵阳", "西藏": "拉萨", "新疆": "乌鲁木齐",
        "青海": "西宁", "甘肃": "兰州", "陕西": "西安", "广东": "广州", "广西": "南宁",
        "海南": "海口", "福建": "福州", "浙江": "杭州", "江苏": "南京", "山东": "济南",
        "台湾": "台北", "北京": "北京", "天津": "天津", "河北": "石家庄", "河南": "郑州",
        "山西": "太原", "内蒙古": "呼和浩特", "黑龙江": "哈尔滨", "吉林": "长春",
        "辽宁": "沈阳", "湖北": "武汉", "湖南": "长沙", "江西": "南昌", "安徽": "合肥",
        "上海": "上海", "重庆": "重庆"
    }

    sql_statements = [
        "-- 自动生成的更新鸟类分布区域 (country, province, city, region) 的 SQL 脚本",
        "SET NAMES utf8mb4;",
        "BEGIN;"
    ]

    # 为了增加演示真实性，这里写死几个 CUB-200 常见鸟类到中国的固定分布，其余仍然随机（如果有AI接口可以全部替换为调用API）
    real_distribution_mock = {
        "Black footed Albatross": ["台湾", "广东", "福建"],
        "Mallard": ["黑龙江", "吉林", "辽宁", "新疆"],
        "Common Raven": ["西藏", "青海", "新疆"],
        "Rusty Blackbird": ["内蒙古", "黑龙江"],
    }

    for idx, raw_name in names_dict.items():
        # 清洗模型中的名字（例如把 "001.Black_footed_Albatross" 转为 "Black footed Albatross"）
        if '.' in raw_name:
            english_name = raw_name.split('.', 1)[1].replace('_', ' ')
        else:
            english_name = raw_name.replace('_', ' ')
            
        if english_name in real_distribution_mock:
            assigned_provs = real_distribution_mock[english_name]
        else:
            # 随机抽取1~3个省份并匹配对应省会城市
            assigned_provs = random.sample(list(prov_city_map.keys()), k=random.randint(1, 3))
            
        assigned_cities = [prov_city_map[p] for p in assigned_provs]
        
        country_str = "中国"
        province_str = ",".join(assigned_provs)
        city_str = ",".join(assigned_cities)
        # 为兼容旧的展现逻辑，仍可把 region 补充下
        region_str = f"中国 {province_str}"

        # 生成 UPDATE 语句，增加对 country, province, city 的更新
        sql = f"UPDATE bird SET country = '{country_str}', province = '{province_str}', city = '{city_str}', region = '{region_str}' WHERE english_name = '{english_name}' OR english_name = '{raw_name}';"
        sql_statements.append(sql)

    sql_statements.append("COMMIT;")

    # 4. 导出为 .sql 文件
    output_path = os.path.join(BASE_DIR, "update_bird_regions.sql")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    print(f"🎉 SQL 脚本已成功生成：{output_path}")
    print("你可以直接在 MySQL 数据库 GUI（如 Navicat/DataGrip）中运行该脚本，或者通过命令行导入！")

if __name__ == "__main__":
    main()


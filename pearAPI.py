import requests

# 通用API Key（无需修改）
API_KEY = "3dbfdd7e8c23d006"

# 各接口地址配置
API_CONFIG = {
    "box_office": "https://api.pearktrue.cn/api/maoyan/",
    "oil_price": "https://api.pearktrue.cn/api/oilprice",
    "daily_hot": "https://api.pearktrue.cn/api/dailyhot/"
}


def get_maoyan_box_office() -> dict:
    """调用PearAPI猫眼电影实时票房接口，获取最新票房排行"""
    params = {"key": API_KEY}
    try:
        response = requests.get(API_CONFIG["box_office"], params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常：{e}")
        return {"code": 500, "msg": f"网络错误：{str(e)}"}


def get_oil_price(province_name: str) -> dict:
    """调用PearAPI今日油价接口，查询指定省份的油价"""
    params = {
        "key": API_KEY,
        "type": "get",
        "province": province_name
    }
    try:
        response = requests.get(API_CONFIG["oil_price"], params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常：{e}")
        return {"code": 500, "msg": f"网络错误：{str(e)}"}


def get_daily_hot(platform_title: str) -> dict:
    """调用PearAPI今日热榜聚合接口，获取指定平台的实时热榜"""
    params = {
        "key": API_KEY,
        "title": platform_title
    }
    try:
        response = requests.get(API_CONFIG["daily_hot"], params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常：{e}")
        return {"code": 500, "msg": f"网络错误：{str(e)}"}


def show_box_office():
    """展示猫眼电影票房前5数据"""
    print("\n=== PearAPI 猫眼电影实时票房排行（仅展示前5名） ===")
    print("正在获取最新票房数据...\n")

    result = get_maoyan_box_office()
    if result.get("code") == 200:
        print(f"✅ 数据获取成功！更新时间：{result.get('time', '未知')}\n")
        movie_list = result.get("data", [])[:5]
        for idx, movie in enumerate(movie_list, 1):
            print(f"🏆 第{idx}名：{movie.get('movieName', '未知电影')}")
            print(f"    总票房：{movie.get('sumBoxDesc', '未知')} | 票房占比：{movie.get('boxRate', '未知')}")
            print(f"    上映天数：{movie.get('releaseInfo', '未知')} | 排片占比：{movie.get('showCountRate', '未知')}")
            print(f"    场均人次：{movie.get('avgShowView', '未知')} | 上座率：{movie.get('avgSeatView', '未知')}\n")
    else:
        print(f"❌ 获取失败，错误信息：{result.get('msg', '未知错误')}")


def show_oil_price():
    """交互式查询并展示指定省份油价"""
    print("\n=== PearAPI 今日油价查询工具 ===")
    print("支持输入：省份/直辖市名称（例如：四川、广东、北京）\n")

    province = input("请输入要查询的省份/直辖市名称：").strip()
    if not province:
        print("❌ 省份名称不能为空！")
        return

    print(f"\n正在获取【{province}】最新油价...\n")
    result = get_oil_price(province)
    if result.get("code") == 200:
        data = result.get("data", {})
        print(f"✅ 查询成功！数据时间：{data.get('time', '未知')}\n")

        province_data = data.get("province", {})
        print(f"📍 查询省份：{province_data.get('pri_name', '未知')}")
        print(f"💰 92#汽油  ：{province_data.get('gasoline_92', '未知')} 元/升")
        print(f"💰 95#汽油  ：{province_data.get('gasoline_95', '未知')} 元/升")
        print(f"💰 98#汽油  ：{province_data.get('gasoline_98', '未知')} 元/升")
        print(f"⛽ 0# 柴油   ：{province_data.get('diesel_0', '未知')} 元/升\n")
    else:
        print(f"❌ 获取失败，错误信息：{result.get('msg', '未知错误')}\n")


def show_daily_hot():
    """交互式查询并展示指定平台热榜"""
    print("\n=== PearAPI 今日热榜聚合查询工具（仅展示前5条） ===")
    print("支持平台：微博、知乎、抖音、B站、百度、CSDN等（输入平台名称即可）\n")

    platform = input("请输入要查询的平台名称：").strip()
    if not platform:
        print("❌ 平台名称不能为空！")
        return

    print(f"\n正在获取【{platform}】实时热榜...\n")
    result = get_daily_hot(platform)
    if result.get("code") == 200:
        print(f"✅ 【{result.get('name', platform)}】热榜获取成功！")
        print(f"更新时间：{result.get('updateTime', '未知')}")
        print(f"共获取{result.get('total', 0)}条热榜，仅展示前5条\n")

        hot_list = result.get("data", [])[:5]
        for idx, item in enumerate(hot_list, 1):
            print(f"{idx:2d}. {item.get('title', '无标题')}")
            print(f"    热度：{item.get('hot', '无热度')} | 链接：{item.get('url', '无链接')}\n")
    else:
        print(f"❌ 获取失败，错误信息：{result.get('msg', '未知错误')}\n")


def main_menu():
    """主菜单"""
    while True:
        print("=" * 50)
        print("          PearAPI 多功能查询工具")
        print("=" * 50)
        print("1. 猫眼电影实时票房查询")
        print("2. 今日油价查询")
        print("3. 平台热榜查询")
        print("0. 退出程序")
        print("=" * 50)

        choice = input("请选择功能（0-3）：").strip()
        if choice == "1":
            show_box_office()
        elif choice == "2":
            show_oil_price()
        elif choice == "3":
            show_daily_hot()
        elif choice == "0":
            print("\n👋 感谢使用，程序已退出！")
            break
        else:
            print("\n❌ 无效选择，请输入0-3之间的数字！\n")

        # 执行完功能后暂停，方便查看结果
        if choice in ["1", "2", "3"]:
            input("按回车键返回主菜单...")


if __name__ == "__main__":
    main_menu()
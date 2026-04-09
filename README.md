# Langchain-agent代理

在Langchain中，Agent代理是⼀种智能化的计算机制，它能够根据输⼊的指令或环境上下⽂，动态选择和调⽤特定的⼯具（如搜索引擎、数据库、API等）来完成任务。

## 实验环境

| 环境配置项      | 参数说明                                   |
| --------------- | ------------------------------------------ |
| 当前激活环境    | RAG                                        |
| Conda版本       | 24.11.3                                    |
| Conda-Build版本 | 24.9.0                                     |
| Python版本      | 3.12.7.final.0                             |
| 硬件配置        | NVIDIA GPU（支持CUDA 12.7，可实现GPU加速） |

## 技术栈

| 分类       | 技术 / 依赖         | 版本 / 用途说明                              |
| ---------- | ------------------- | -------------------------------------------- |
| 开发语言   | Python              | 3.8 及以上，项目运行基础环境                 |
| 网络请求   | requests            | 用于调用心知天气、PearAPI 等第三方接口       |
| 数据校验   | pydantic            | 工具入参格式校验、字段规范约束               |
| 代理框架   | LangChain           | 实现智能 Agent、工具封装、推理链路管理       |
| 模型对接   | LangChain-OpenAI    | 兼容 OpenAI 协议，对接大模型接口             |
| 大模型     | Qwen2.5-7B-Instruct | 硅基流动平台提供，用于推理、决策与回答生成   |
| 数据源 API | PearAPI             | 提供猫眼票房、今日油价、今日热榜三大查询能力 |
| 数据源 API | 心知天气            | 提供全国城市实时天气、温度查询服务           |

## 功能列表

| 模块     | 核心功能                                      | 依赖 API     |
| -------- | --------------------------------------------- | ------------ |
| 天气查询 | 实时查询指定城市天气 / 温度，支持智能代理交互 | 心知天气 API |
| 票房查询 | 猫眼电影实时票房排行（前 5 名）               | PearAPI      |
| 油价查询 | 按省份查询 92/95/98 号汽油、0 号柴油价格      | PearAPI      |
| 热榜查询 | 多平台实时热榜（微博 / 知乎 / 抖音 / B 站等） | PearAPI      |

### 环境配置

#### 安装依赖

```
pip install requests
pip install pydantic
pip install langchain
pip install langchain-openai
```

### API Key 配置（重要）

1. #### 配置 API 密钥

   代码中的 **心知天气 API Key**（`api_key` 变量）：需前往[心知天气官网](https://www.seniverse.com/)申请免费API 密钥：

   ```
   api_key = "你的心知天气KEY"
   ```

2. #### 大模型API Key

   在 `agent.py` 中替换硅基流动 API Key：

   ```
   openai_api_key="你的硅基流动KEY"
   ```

3. #### PearAPI Key

   在 `pearAPI.py` 中已内置可用 Key：

   ```
   API_KEY = "你的PearAPI的API Key"
   ```

### 心知天气（agent.py）

```
 # 构建 API 请求 URL 返回结果
        response = requests.get(url)
        if response.status_code == 200: # 请求成功
            data = response.json() # 解析返回的JSON
            weather = data["results"][0]["now"]["text"] # 天气信息
            tem = data["results"][0]["now"]["temperature"] # 温度
            return f"{city}的天气是{weather}, 温度是{tem}°C" # 返回格式化后的天气信息
        else:
            return f"无法获取{city}的天气信息。"
```

### 大模型(agent.py)

```
from langchain_openai import ChatOpenAI
chat_model = ChatOpenAI(
    openai_api_key="sk-hyoifmdpfblaiceviubonrgwudsexzkukoznafmcjuxezyrx", # ollama兼容OpenAIAPI的格式
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct"
)
```

### PearAPI (pearAPI.py)

##### 配置各接口地址

```
# 各接口地址配置
API_CONFIG = {
    "box_office": "https://api.pearktrue.cn/api/maoyan/",
    "oil_price": "https://api.pearktrue.cn/api/oilprice",
    "daily_hot": "https://api.pearktrue.cn/api/dailyhot/"
}
```

##### 调用PearAPI

```
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

```

### 输出展示

##### agent.py

<img width="1726" height="574" alt="屏幕截图 2026-04-09 104632" src="https://github.com/user-attachments/assets/4e0915fb-2ae9-4695-a10c-3404abd413fc" />

##### pearAPI.py

<img width="1321" height="523" alt="屏幕截图 2026-04-09 104644" src="https://github.com/user-attachments/assets/342c9e4a-6575-4e0f-9e3d-463aff4281b3" />

<img width="738" height="711" alt="屏幕截图 2026-04-09 104658" src="https://github.com/user-attachments/assets/a25115d8-488f-492b-a23a-6cefb8b2e2d7" />

<img width="766" height="723" alt="屏幕截图 2026-04-09 104738" src="https://github.com/user-attachments/assets/020bae30-4093-4b4b-8c69-0f4fcea2ce65" />

<img width="769" height="731" alt="屏幕截图 2026-04-09 104809" src="https://github.com/user-attachments/assets/d0b76e30-ad86-434e-bf26-beb5baf132fe" />

<img width="1913" height="924" alt="屏幕截图 2026-04-09 104824" src="https://github.com/user-attachments/assets/b34c0fd3-e376-472a-819f-b3eb9c8f70c1" />


- ## 注意事项

  1. **API 调用次数限制**：免费额度有限，请勿高频调用
  2. **网络要求**：确保可正常访问 [api.pearktrue.cn](https://api.pearktrue.cn)、[api.seniverse.com](https://api.seniverse.com)
  3. 输入规范：
     - 油价：输入省份名称（如：四川）
     - 热榜：输入平台名（如：微博）
     - 天气：输入城市名（如：成都）
  4. **密钥安全**：正式部署请使用环境变量存储 KEY，不要硬编码上传至仓库
